from enum import Enum

class Provider(Enum):
    """
    Enum for different llm providers.
    """
    OPENROUTER = "openrouter"
    GEMINI = "gemini"
    OPENAI = "openai"

class OpenRouterModel(Enum):
    """
    Enum for different OpenRouter models.
    """
    LLAMA_4_MAVERICK = "meta-llama/llama-4-maverick:free"
    LLAMA_3 = "meta-llama/llama-3:free"
    LLAMA_2 = "meta-llama/llama-2:free"
    LLAMA_1 = "meta-llama/llama-1:free"
    OPT = "facebook/opt:free"
    BLOOM = "bigscience/bloom:free"
    GPT_J = "EleutherAI/gpt-j:free"

class GeminiModel(Enum):
    """
    Enum for different Gemini models.
    """
    GEMINI_2_5 = "gemini-2.5"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_1_5 = "gemini-1.5"
    GEMINI_1_0 = "gemini-1.0"

class OpenAIModel(Enum):
    """
    Enum for different OpenAI models.
    """
    GPT_4 = "gpt-4"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_16K = "gpt-3.5-turbo-16k"
    GPT_3 = "gpt-3"
    DALL_E = "dall-e"
    WHISPER = "whisper"