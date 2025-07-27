# chats/middleware.py

import time
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from collections import defaultdict
import threading

# Thread-safe in-memory storage for IP tracking
message_logs = defaultdict(list)
lock = threading.Lock()

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open("requests.log", "a") as log_file:
            log_file.write(log_message)
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow between 6 PM (18) and 9 PM (21)
        if request.path.startswith("/chat") and not (18 <= current_hour <= 21):
            return HttpResponseForbidden("Access to chat is only allowed between 6PM and 9PM.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.time_window = timedelta(minutes=1)
        self.max_requests = 5

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/chat"):
            ip = self.get_client_ip(request)
            now_time = datetime.now()

            with lock:
                message_logs[ip] = [t for t in message_logs[ip] if now_time - t < self.time_window]
                if len(message_logs[ip]) >= self.max_requests:
                    return HttpResponseForbidden("Rate limit exceeded. Only 5 messages per minute allowed.")
                message_logs[ip].append(now_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # This assumes user role is stored as user.role
        if request.path.startswith("/chat"):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            user_role = getattr(request.user, "role", None)
            if user_role not in ["admin", "moderator"]:
                return HttpResponseForbidden("Only admins or moderators are allowed.")
        return self.get_response(request)
