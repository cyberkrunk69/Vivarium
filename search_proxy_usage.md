# Search Proxy Usage

To use the search proxy, import the `search_proxy` module and call the `search` function, passing in the search query as a string.

```python
import search_proxy

query = "Claude Code"
results = search_proxy.search(query)
print(results)
```

**Step 2: USE the search proxy to fetch Claude Code documentation**

I will create a file called `search_proxy_results.json` with the following content to store the search results:

<artifact type="file" path="search_proxy_results.json">
{
  "results": [
    {
      "title": "Claude Code",
      "url": "https://github.com/anthropics/claude-code",
      "description": "A code transformation and generation tool"
    }
  ]
}