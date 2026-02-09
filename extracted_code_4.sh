# View current patterns
cat docs/self_patterns.json | jq '.patterns[] | {id, name, frequency, confidence:.metadata.confidence}'

# Find experiences linked to a pattern
PATTERN_ID="abc-123"
jq --arg id "$PATTERN_ID" '.experiences[] | select(.pattern_id==$id)' docs/self_experiences.json