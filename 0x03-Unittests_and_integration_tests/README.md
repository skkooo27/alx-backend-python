# 0x03. Unittests and Integration Tests

This project focuses on writing unit tests and integration tests for Python backend utilities.

## Project Structure

-utils.py: Contains utility functions like `access_nested_map`, `get_json`, and `memoize`.
-test_utils.py: Contains unit tests for functions in `utils.py`.
-clients.py: Defines a GitHub organization client class.
-test_client.py: Contains unit and integration tests for the GitHubOrgClient class.
-fixtures.py: Contains pre-defined JSON data used in integration tests.

## Technologies Used

- Python 3
- unittest
- parameterized
- requests library
- unittest.mock (patching and mocking)

## How to Run Tests

From the project directory:
```bash
python -m unittest test_utils.py
python -m unittest test_client.py
