class AgentContext:
    """
    Context for the agent, containing the agent's name and description.
    """

    output_path = ""

    def __init__(self, output_path: str = ""):
        self.output_path = output_path
