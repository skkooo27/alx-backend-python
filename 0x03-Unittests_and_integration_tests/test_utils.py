#!/usr/bin/env python3
"""Unit tests for access_nested_map in utils.py."""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch
from utils import get_json



class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns correct result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised when path is invalid."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(cm.exception.args[0], path[-1])

class TestGetJson(unittest.TestCase):
    """Tests for get_json function."""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """Test get_json returns correct payload."""
        test_payload = {"payload": True}
        test_url = "http://example.com"

        mock_get.return_value.json.return_value = test_payload

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)
