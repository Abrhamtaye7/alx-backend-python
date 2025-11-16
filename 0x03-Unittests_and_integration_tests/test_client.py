#!/usr/bin/env python3
from unittest import TestCase
from unittest.mock import patch
import unittest
from client import GithubOrgClient
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class  # <-- make sure this is here
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos



class TestGithubOrgClient(TestCase):
    """Task 4: Test GithubOrgClient.org method."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test org returns the correct value."""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )


    def test_public_repos_url(self):
        """Test correct repos_url from org payload"""
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = org_payload
            client = GithubOrgClient("google")
            expected = org_payload["repos_url"]
            self.assertEqual(client._public_repos_url, expected)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns correct repo list"""
        mock_get_json.return_value = repos_payload
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = org_payload["repos_url"]
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), expected_repos)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license helper"""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


class MockResponse:
    """Mock response object for .json()"""

    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def get_json_side_effect(url):
            if url.endswith("/orgs/google"):
                return MockResponse(cls.org_payload)
            if url.endswith("/orgs/google/repos"):
                return MockResponse(cls.repos_payload)
            return MockResponse(None)

        mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos integration"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test license filtering integration"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )
