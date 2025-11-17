#!/usr/bin/env python3
"""
Task 4 and Task 5: Unit tests for GithubOrgClient.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected result."""
        payload = {"login": org_name}
        mock_get_json.return_value = payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected value."""
        payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload

            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                payload["repos_url"]
            )


if __name__ == "__main__":
    unittest.main()
