from typing import List
import json


class AgentContext:
    """
    Context for the agent, containing the agent's name and description.
    """

    output_path = ""
    column_names: List[str] = []

    def __init__(self, output_path: str = ""):
        self.output_path = output_path
        self.column_names = []

    def input_column_names(self, csv_header: str):
        """
        入力されたCSVヘッダー行（カンマ区切り）からカラム名リストを登録する。
        改行以降は無視する。
        """
        first_line = csv_header.splitlines()[0] if csv_header else ""
        self.column_names = [
            col.strip() for col in first_line.split(",") if col.strip()
        ]

    def json_to_csv_row(self, data: dict) -> str:
        """
        column_names順にdata(dict)から値を取り出し、CSVの1行として返す。
        値がなければ空欄。値にカンマや改行が含まれる場合は"で囲む。
        """

        def escape(val):
            if val is None:
                return ""
            s = str(val)
            if "," in s or "\n" in s or '"' in s:
                s = '"' + s.replace('"', '""') + '"'
            return s

        return ",".join(escape(data.get(col, "")) for col in self.column_names)
