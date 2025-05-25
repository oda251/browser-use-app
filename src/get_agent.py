from browser_use import Agent, BrowserConfig
from src.get_llm import LLMConfig, get_llm
from src.get_controller import get_controller
from src.entity.controller_type import OutputFormat


def get_agent(
    instruction: str,
    llm_config: LLMConfig,
    browser_profile: BrowserConfig,
    output_format: OutputFormat = OutputFormat.MARKDOWN,
    output_dir: str = "output",
    should_stop=None,  # 追加
) -> Agent[None]:
    """
    Get the agent instance with the specified task and controller.
    """
    agent = Agent[None](
        task=instruction,
        llm=get_llm(config=llm_config),
        controller=get_controller(
            output_format=output_format,
            ouput_dir=output_dir,
        ),
        browser_profile=browser_profile,
    )
    # Agentにshould_stopをセットできる場合
    if should_stop is not None:
        setattr(agent, "should_stop", should_stop)
    return agent
