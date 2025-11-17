
#!/usr/bin/env python3
"""
Task 4, 5, 6: Unit tests for GithubOrgClient.
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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected repo names."""
        repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = repos_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = (
                "https://api.github.com/orgs/google/repos"
            )

            client = GithubOrgClient("google")
            result = client.public_repos()

        self.assertEqual(result, ["repo1", "repo2", "repo3"])
        mock_get_json.assert_called_once()
        mock_url.assert_called_once()


if __name__ == "__main__":
    unittest.main()
