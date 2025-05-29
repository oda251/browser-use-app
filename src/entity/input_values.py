from enum import Enum


class InstructionInputKey(Enum):
    PURPOSE = "instruction_purpose"
    DETAIL = "instruction_detail"
    REFERENCE_URL = "instruction_reference_url"
    COMMON_INSTRUCTION = "instruction_common_instruction"
    DATA_ITEMS = "instruction_data_items"
    OUTPUT_FORMAT = "instruction_output_format"


class LLMInputKey(Enum):
    PROVIDER = "llm_provider"
    MODEL = "llm_model"
    API_KEY = "llm_api_key"


class BrowserInputKey(Enum):
    HEADLESS = "browser_headless"
    KEEP_ALIVE = "browser_keep_alive"


class OutputInputKey(Enum):
    OUTPUT_DIR = "output_output_dir"


class ButtonInputKey(Enum):
    # ボタン自体は値を持たないが、必要ならここに追加
    pass
