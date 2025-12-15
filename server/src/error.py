class QueryParseError(Exception):
    """User input could not be parsed into required fields"""

    pass


class LLMServiceError(Exception):
    """OpenAI or infrastructure failure"""

    pass
