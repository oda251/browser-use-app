from browser_use import Agent, BrowserConfig
from src.get_llm import LLMConfig, get_llm
from typing import List
from src.get_controller import get_controller, ControllerType

def get_agent(
    instruction: str,
    llm_config: LLMConfig,
    browser_profile: BrowserConfig,
    controller_types: List[ControllerType] = [ControllerType.MARKDOWN],
    output_dir: str = "output",
) -> Agent[None]:
    """
    Get the agent instance with the specified task and controller.
    """
    return Agent[None](
        task=instruction,
        llm=get_llm(config=llm_config),
        controller=get_controller(
            controller_types=controller_types,
            ouput_dir=output_dir,
        ),
        browser_profile=browser_profile
    )
