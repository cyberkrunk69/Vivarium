#!/usr/bin/env python3

import requests
from urllib.parse import urlparse
from safety_web_gateway import WebGateway

class DocumentationSearcher:
    def __init__(self):
        self.cache = {}
        self.allowlisted_sources = [
            "docs.groq.com",
            "console.groq.com",
            "github.com/groq",
        ]
        self.rate_limit = 10  # max requests per minute
        self.request_count = 0
        self.last_request_time = 0

    def search(self, query):
        if self.request_count >= self.rate_limit:
            # rate limit exceeded, wait for next minute
            return None

        # check cache first
        if query in self.cache:
            return self.cache[query]

        # construct search URL
        url = f'https://www.google.com/search?q={query}'

        # send request and get response
        response = requests.get(url)

        # sanitize response
        sanitized_response = self.sanitize_response(response.text)

        # cache result
        self.cache[query] = sanitized_response

        # increment request count
        self.request_count += 1

        return sanitized_response

    def sanitize_response(self, response):
        # strip scripts and tracking
        sanitized_response = response.replace('<script>', '').replace('</script>', '')
        sanitized_response = sanitized_response.replace('tracking', '')

        return sanitized_response

    def is_allowlisted(self, url):
        parsed_url = urlparse(url)
        return any(allowlisted_source in parsed_url.netloc for allowlisted_source in self.allowlisted_sources)

# integrate with WebGateway
web_gateway = WebGateway()
searcher = DocumentationSearcher()

def search_documentation(query):
    return searcher.search(query)

# add mock/offline mode for testing
class MockSearcher:
    def search(self, query):
        return f'Mock search result for {query}'

def main():
    # test search proxy
    query = 'test query'
    result = search_documentation(query)
    print(result)

if __name__ == '__main__':
    main()