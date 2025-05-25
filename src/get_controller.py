from browser_use import Controller
import os
from src.entity.controller_type import OutputFormat
from src.entity.agent_context import AgentContext


def get_controller(
    output_format: OutputFormat = OutputFormat.MARKDOWN,
    ouput_dir: str = "output",
) -> Controller[AgentContext]:
    """
    Get the controller instance based on the specified output format.
    """
    if not os.path.exists(ouput_dir):
        os.makedirs(ouput_dir)
    controller = Controller[AgentContext]()

    match output_format:
        case OutputFormat.MARKDOWN:

            @controller.action(
                """
                Create a markdown file.
                ARGS:
                    title (str): The title of the file.
                    content (str): The content to be written to the file. Extension is not needed.
                    context (AgentContext): This is injected automatically; you do not need to provide it.
                """
            )
            def create_markdown(title: str, content: str, context: AgentContext):
                path = os.path.join(ouput_dir, f"{title}.md")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                context.output_path = path

            @controller.action(
                """
                Append content to a markdown file.
                ARGS:
                    content (str): The content to append.
                    context (AgentContext): This is injected automatically; you do not need to provide it.
                """
            )
            def append_markdown(content: str, context: AgentContext):
                path = context.output_path
                with open(path, "a", encoding="utf-8") as f:
                    f.write(content)

        case OutputFormat.TEXT:

            @controller.action(
                """
                Create a plain text file.
                ARGS:
                    title (str): The title (filename, without extension) for the text file to save.
                    content (str): The content to be written to the file. Extension is not needed.
                    context (AgentContext): This is injected automatically; you do not need to provide it.
                """
            )
            def create_text(title: str, content: str, context: AgentContext):
                path = os.path.join(ouput_dir, f"{title}.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                context.output_path = path

            @controller.action(
                """
                Append content to a text file.
                ARGS:
                    content (str): The content to append.
                    context (AgentContext): This is injected automatically; you do not need to provide it.
                """
            )
            def append_text(content: str, context: AgentContext):
                path = context.output_path
                with open(path, "a", encoding="utf-8") as f:
                    f.write(content)

        case OutputFormat.CSV:

            @controller.action(
                """
                Create a CSV file.
                ARGS:
                    title (str): The title of the file.
                    content (str): The content to be written to the file. Extension is not needed.
                    context (AgentContext): This is injected automatically; you do not need to provide it.
                """
            )
            def create_csv(title: str, content: str, context: AgentContext):
                path = os.path.join(ouput_dir, f"{title}.csv")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                context.output_path = path
                context.input_column_names(content)

            @controller.action(
                """
                Append a list of JSON objects to a CSV file.
                ARGS:
                    content (list): List of JSON objects to append as CSV rows. Each object must have all the specified data item keys as string values. Example: [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
                    context (AgentContext): This is injected automatically; you do not need to provide it.
                """
            )
            def append_csv(content: list[dict[str, str]], context: AgentContext):
                path = context.output_path
                with open(path, "a", encoding="utf-8") as f:
                    for item in content:
                        row = context.json_to_csv_row(item)
                        f.write(row)

    return controller
