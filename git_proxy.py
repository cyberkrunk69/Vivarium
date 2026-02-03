#!/usr/bin/env python3

import git
import logging

class GitReadOnlyProxy:
    def __init__(self, repository_allowlist):
        self.repository_allowlist = repository_allowlist

    def clone(self, repository_url):
        if repository_url in self.repository_allowlist:
            git.Repo.clone_from(repository_url, '--depth', '1')
            logging.info(f"Cloned {repository_url} with shallow clone")
        else:
            logging.warning(f"Clone operation blocked for {repository_url}")

    def fetch(self, repository_url):
        if repository_url in self.repository_allowlist:
            git.Repo(repository_url).remotes.origin.fetch()
            logging.info(f"Fetched {repository_url}")
        else:
            logging.warning(f"Fetch operation blocked for {repository_url}")

    def pull(self, repository_url):
        if repository_url in self.repository_allowlist:
            git.Repo(repository_url).remotes.origin.pull()
            logging.info(f"Pulled {repository_url}")
        else:
            logging.warning(f"Pull operation blocked for {repository_url}")

    def ls_remote(self, repository_url):
        if repository_url in self.repository_allowlist:
            git.Repo(repository_url).remotes.origin.ls_remote()
            logging.info(f"Performed ls-remote on {repository_url}")
        else:
            logging.warning(f"ls-remote operation blocked for {repository_url}")

    def push(self, repository_url):
        logging.warning(f"Push operation blocked for {repository_url}")
        raise Exception("Push operation is not allowed")

    def force_push(self, repository_url):
        logging.warning(f"Force-push operation blocked for {repository_url}")
        raise Exception("Force-push operation is not allowed")

    def delete_remote(self, repository_url):
        logging.warning(f"Delete remote operation blocked for {repository_url}")
        raise Exception("Delete remote operation is not allowed")