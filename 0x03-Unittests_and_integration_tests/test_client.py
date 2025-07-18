#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value."""
        test_payload = {"payload": True}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL."""
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }

            client = GithubOrgClient("test_org")
            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/test/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected repo names."""
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_payload

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"

            client = GithubOrgClient("test_org")
            result = client.public_repos()

            expected = ["repo1", "repo2", "repo3"]

            self.assertEqual(result, expected)
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos"
            )
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method returns correct boolean."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],    # First item in first tuple
        "repos_payload": TEST_PAYLOAD[0][1],  # Second item in first tuple
        "expected_repos": [repo["name"] for repo in TEST_PAYLOAD[0][1]],
        "apache2_repos": [
            repo["name"]
            for repo in TEST_PAYLOAD[0][1]
            if (repo.get("license") or {}).get("key") == "apache-2.0"
        ],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get using fixtures."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        mock_get.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload,
            cls.org_payload,
            cls.repos_payload,
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names."""
        client = GithubOrgClient("test_org")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filtering."""
        client = GithubOrgClient("test_org")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
