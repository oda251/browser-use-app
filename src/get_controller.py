from browser_use import Controller
from typing import List
import os
from src.entity.controller_type import ControllerType

def get_controller(
        contoller_types: List[ControllerType] = [ControllerType.MARKDOWN],
        ouput_dir: str = "output",
):
    """
    Get the controller instance based on the specified controller types.
    """
    if not os.path.exists(ouput_dir):
        os.makedirs(ouput_dir)
    controller = Controller()

    for controller_type in contoller_types:
        match controller_type:
            case ControllerType.MARKDOWN:
                @controller.action("Document a file in markdown format")
                def write_markdown(title: str, content: str):
                    """
                    Write the content to a file in markdwon format with the given title.
                    ARGS:
                        title (str): The title of the file.
                        content (str): The content to be written to the file.
                    """
                    path = os.path.join(ouput_dir, f"{title}.md")
                    with open(path, "w") as f:
                        f.write(content)
            case ControllerType.IMAGE:
                @controller.action("")
                def save_image(title: str, content: bytes) -> str:
                    """
                    Save an image with the given title.
                    Returns the path to the file.
                    ARGS:
                        title (str): The title of the file.
                        content (bytes): The content of the image.
                    RETURNS:
                        str: The path to the file.
                    """
                    path = os.path.join(ouput_dir, f"{title}.png")
                    with open(path, "wb") as f:
                        f.write(content)
                    return path
    return controller
