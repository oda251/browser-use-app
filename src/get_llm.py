from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
import os


class LLMConfig:
    """
    Configuration class for LLM.
    """

    def __init__(self, provider: str, model: str, api_key: str):
        self.provider = provider
        self.model = model
        self.api_key = api_key


def get_llm(config: LLMConfig):
    """
    Get the LLM instance based on the specified configuration.
    """
    match config.provider:
        case "openrouter":
            return _get_openrouter_llm(config.model)
        case "openai":
            return _get_openai_llm(config.model)
        case "google":
            return _get_google_llm(config.model)
        case _:
            raise ValueError(f"Unsupported LLM provider: {config.provider}")


def _get_openrouter_llm(
    model: str = "meta-llama/llama-4-maverick:free",
) -> ChatOpenAI:
    """
    Get the OpenRouter LLM instance.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEYが環境変数に設定されていません")
    return ChatOpenAI(
        model=model,
        api_key=SecretStr(api_key),
        base_url="https://api.openrouter.ai/v1",
        temperature=0,
    )


def _get_openai_llm(
    model: str = "gpt-3.5-turbo",
) -> ChatOpenAI:
    """
    Get the OpenAI LLM instance.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEYが環境変数に設定されていません")
    return ChatOpenAI(
        model=model,
        api_key=SecretStr(api_key),
        temperature=0,
    )


def _get_google_llm(
    model: str = "gemini-2.0-flash",
) -> ChatGoogleGenerativeAI:
    """
    Get the Google LLM instance.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEYが環境変数に設定されていません")
    return ChatGoogleGenerativeAI(
        model=model,
        api_key=SecretStr(api_key),
        temperature=0,
    )
