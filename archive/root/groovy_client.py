class GroovyClient:
    """
    Simple client that maps model identifiers to their corresponding
    Groovy (Groq) model names. In a real implementation this would
    handle authentication, request construction, and response parsing.
    """

    # Mapping from our internal identifiers to the actual Groq model IDs
    MODEL_MAP = {
        "llama-3.1-8b-instant": "llama-3.1-8b-instant",
        "openai/gpt-oss-20b": "openai/gpt-oss-20b",
        "llama-3.3-70b-versatile": "llama-3.3-70b-versatile",
        "openai/gpt-oss-120b": "openai/gpt-oss-120b",
    }

    def __init__(self, api_key: str):
        self.api_key = api_key
        # In a real client you would set up HTTP session, headers, etc.

    def get_model_id(self, internal_name: str) -> str:
        """
        Translate an internal model name (as returned by
        ``complexity_detector.detect_complexity``) into the actual
        Groq model identifier.
        """
        return self.MODEL_MAP.get(internal_name, internal_name)

    # Placeholder for a real request method
    def request(self, model_name: str, prompt: str) -> str:
        """
        Send a request to the Groq API. This stub simply returns a
        formatted string for demonstration purposes.
        """
        model_id = self.get_model_id(model_name)
        # Here you would normally perform an HTTP request.
        return f"Request sent to model {model_id} with prompt: {prompt}"