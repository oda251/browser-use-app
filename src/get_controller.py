from browser_use import Controller
from typing import List
import os
from src.entity.controller_type import ControllerType


def get_controller(
    controller_types: List[ControllerType] = [ControllerType.MARKDOWN],
    ouput_dir: str = "output",
) -> Controller[None]:
    """
    Get the controller instance based on the specified controller types.
    """
    if not os.path.exists(ouput_dir):
        os.makedirs(ouput_dir)
    controller = Controller[None]()

    for controller_type in controller_types:
        match controller_type:
            case ControllerType.MARKDOWN:

                @controller.action(
                    """
                    Document a file in markdown format.
                    ARGS:
                        title (str): The title of the file.
                        content (str): The content to be written to the file.
                    RETURNS:
                        str: The path to the file.
                    """
                )
                def write_markdown(title: str, content: str) -> str:
                    """
                    Write the content to a file in markdwon format with the given title.
                    ARGS:
                        title (str): The title of the file.
                        content (str): The content to be written to the file.
                    """
                    path = os.path.join(ouput_dir, f"{title}.md")
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    return path

            case ControllerType.IMAGE:

                @controller.action(
                    """
                    Save an image file in PNG format.
                    ARGS:
                        title (str): The title (filename, without extension) for the image file to save.
                        content (bytes): The binary content of the image (PNG format recommended).
                    RETURNS:
                        str: The full path to the saved image file.
                    DESCRIPTION:
                        This tool saves the given image content as a PNG file in the specified output directory. The file will be named as '<title>.png'. Use this tool to persist images generated or processed by the agent. The function returns the full path to the saved file.
                    """
                )
                def save_image(title: str, content: bytes) -> str:
                    """
                    Save an image with the given title as a PNG file.
                    Args:
                        title (str): The title (filename, without extension) for the image file to save.
                        content (bytes): The binary content of the image (PNG format recommended).
                    Returns:
                        str: The full path to the saved image file.
                    """
                    path = os.path.join(ouput_dir, f"{title}.png")
                    with open(path, "wb") as f:
                        f.write(content)
                    return path

    return controller
