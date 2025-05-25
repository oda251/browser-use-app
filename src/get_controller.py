from browser_use import Controller
import os
from src.entity.controller_type import OutputFormat


def get_controller(
    output_format: OutputFormat = OutputFormat.MARKDOWN,
    ouput_dir: str = "output",
) -> Controller[None]:
    """
    Get the controller instance based on the specified output format.
    """
    if not os.path.exists(ouput_dir):
        os.makedirs(ouput_dir)
    controller = Controller[None]()

    match output_format:
        case OutputFormat.MARKDOWN:

            @controller.action(
                """
                Create a markdown file.
                ARGS:
                    title (str): The title of the file.
                    content (str): The content to be written to the file. Extension is not needed.
                RETURNS:
                    str: The path to the file.
                """
            )
            def create_markdown(title: str, content: str) -> str:
                path = os.path.join(ouput_dir, f"{title}.md")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                return path

            @controller.action(
                """
                Append content to a markdown file.
                ARGS:
                    filename (str): The filename (with .md extension) to append to.
                    content (str): The content to append.
                RETURNS:
                    str: The path to the file.
                """
            )
            def pushback_markdown(filename: str, content: str) -> str:
                path = os.path.join(ouput_dir, filename)
                with open(path, "a", encoding="utf-8") as f:
                    f.write(content)
                return path

        case OutputFormat.TEXT:

            @controller.action(
                """
                Create a plain text file.
                ARGS:
                    title (str): The title (filename, without extension) for the text file to save.
                    content (str): The content to be written to the file. Extension is not needed.
                RETURNS:
                    str: The full path to the saved text file.
                """
            )
            def create_text(title: str, content: str) -> str:
                path = os.path.join(ouput_dir, f"{title}.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                return path

            @controller.action(
                """
                Append content to a text file.
                ARGS:
                    filename (str): The filename (with .txt extension) to append to.
                    content (str): The content to append.
                RETURNS:
                    str: The path to the file.
                """
            )
            def pushback_text(filename: str, content: str) -> str:
                path = os.path.join(ouput_dir, filename)
                with open(path, "a", encoding="utf-8") as f:
                    f.write(content)
                return path

        case OutputFormat.CSV:

            @controller.action(
                """
                Create a CSV file.
                ARGS:
                    title (str): The title of the file.
                    content (str): The content to be written to the file. Extension is not needed.
                RETURNS:
                    str: The path to the file.
                """
            )
            def create_csv(title: str, content: str) -> str:
                path = os.path.join(ouput_dir, f"{title}.csv")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                return path

            @controller.action(
                """
                Append content to a CSV file.
                ARGS:
                    filename (str): The filename (with .csv extension) to append to.
                    content (str): The content to append.
                RETURNS:
                    str: The path to the file.
                """
            )
            def pushback_csv(filename: str, content: str) -> str:
                path = os.path.join(ouput_dir, filename)
                with open(path, "a", encoding="utf-8") as f:
                    f.write(content)
                return path

    return controller
