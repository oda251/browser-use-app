from browser_use import Agent, BrowserConfig
from src.get_llm import LLMConfig, get_llm
from src.get_controller import get_controller
from src.entity.controller_type import OutputFormat
from src.entity.agent_context import AgentContext


def get_agent(
    instruction: str,
    llm_config: LLMConfig,
    browser_profile: BrowserConfig,
    output_format: OutputFormat = OutputFormat.MARKDOWN,
    output_dir: str = "output",
    message_context: str = "",
    context: AgentContext | None = None,
) -> Agent[AgentContext]:
    """
    Get the agent instance with the specified task and controller.
    """
    agent = Agent[AgentContext](
        task=instruction,
        message_context=message_context,
        context=context,
        llm=get_llm(config=llm_config),
        controller=get_controller(
            output_format=output_format,
            ouput_dir=output_dir,
        ),
        browser_profile=browser_profile,
    )
    return agent
