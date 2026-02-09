# Knowledge Packs Design
## Category Taxonomy
The following categories have been identified for the knowledge packs:

* `claude`: Optimal Claude Code techniques, prompting patterns
* `groq`: Groq-specific optimizations, Llama quirks
* `api:spotify`: Spotify API knowledge
* `api:github`: GitHub API patterns
* `safety`: Security lessons
* `ui`: Frontend/dashboard patterns

## Auto-Tagging Algorithm
The auto-tagging algorithm uses a combination of natural language processing (NLP) and keyword extraction to detect the domain of a lesson. The algorithm is implemented in the `auto_tagging.py` file.

## Retrieval API Design
The retrieval API will use a semantic similarity search to retrieve relevant knowledge packs. The API will take a task text as input and return a list of relevant knowledge packs.

## Integration with Spawner
The knowledge packs will be integrated with the spawner using a REST API. The spawner will send a request to the knowledge pack API with the task text, and the API will return a list of relevant knowledge packs.