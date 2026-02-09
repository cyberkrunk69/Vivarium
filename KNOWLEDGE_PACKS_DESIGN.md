# Category Taxonomy
The categories for knowledge packs are:
* claude: Optimal Claude Code techniques, prompting patterns
* groq: Groq-specific optimizations, Llama quirks
* api:spotify: Spotify API knowledge
* api:github: GitHub API patterns
* safety: Security lessons
* ui: Frontend/dashboard patterns

# Auto-tagging Algorithm
The auto-tagging algorithm uses regular expressions to detect the domain of each lesson.

# Retrieval API Design
The retrieval API design uses a simple text search to find relevant lessons.

# Integration with Spawner
The integration with spawner will be done by modifying the `grind_spawner.py` file to use the retrieval API.