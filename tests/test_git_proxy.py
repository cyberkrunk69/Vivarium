#!/usr/bin/env python3

import unittest
from git_proxy import GitReadOnlyProxy

class TestGitProxy(unittest.TestCase):
    def test_push_blocked(self):
        git_proxy = GitReadOnlyProxy(["https://example.com/repository"])
        with self.assertRaises(Exception):
            git_proxy.push("https://example.com/repository")

    def test_force_push_blocked(self):
        git_proxy = GitReadOnlyProxy(["https://example.com/repository"])
        with self.assertRaises(Exception):
            git_proxy.force_push("https://example.com/repository")

    def test_delete_remote_blocked(self):
        git_proxy = GitReadOnlyProxy(["https://example.com/repository"])
        with self.assertRaises(Exception):
            git_proxy.delete_remote("https://example.com/repository")