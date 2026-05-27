
from pydantic import BaseModel


class LLMSettings(BaseModel):
    """
    LLMSettings is a Pydantic model that defines the settings for a language model.
    """

    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0