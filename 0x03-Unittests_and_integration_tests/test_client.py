#!/usr/bin/env python3
"""
Test module for GithubOrgClient
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import org_payload, repos_payload


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected, mock_get):
        """Test that GithubOrgClient.org returns correct data"""
        mock_get.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url returns correct URL"""
        mock_org.return_value = {"repos_url": "http://fakeurl.com"}
        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, "http://fakeurl.com")

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_url, mock_get):
        """Test public_repos returns repo names list"""
        mock_url.return_value = "http://fakeurl.com"
        mock_get.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient with fixtures"""

    @classmethod
    def setUpClass(cls):
        """Setup a client instance and patch get_json for all tests"""
        def side_effect(url):
            if "repos" in url:
                return repos_payload  # Must be a list of dicts
            return org_payload      # Must be a dict

        cls.get_patcher = patch("client.get_json", side_effect=side_effect)
        cls.mock_get = cls.get_patcher.start()
        cls.client = GithubOrgClient("google")

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: public_repos returns expected repo list"""
        repos = self.client.public_repos()
        self.assertEqual(repos, [r["name"] for r in repos_payload])

    def test_public_repos_with_license(self):
        """Integration test: public_repos filters repos by license"""
        filtered = self.client.public_repos(license="my_license")
        expected = [
            r["name"]
            for r in repos_payload
            if r.get("license") and r["license"].get("key") == "my_license"
        ]
        self.assertEqual(filtered, expected)


if __name__ == "__main__":
    unittest.main()
