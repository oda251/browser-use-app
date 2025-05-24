from src.entity.controller_type import OutputFormat


def compose_instruction(
    purpose: str,
    detail: str,
    reference_url: str | None,
    controller_type: OutputFormat | None,
    data_items: list[str] | None = None,
) -> str:
    parts = []
    if purpose:
        parts.append(f"【目的】\n{purpose}")
    if detail:
        parts.append(f"【詳細】\n{detail}")
    if reference_url:
        parts.append(f"【参考URL】\n{reference_url}")
    if data_items:
        filtered = [item for item in data_items if item.strip() != ""]
        if filtered:
            parts.append("【データ項目】\n- " + "\n- ".join(filtered))
    if controller_type:
        match controller_type:
            case OutputFormat.MARKDOWN:
                parts.append(
                    "【出力形式】\n出力は見やすく構造化されたMarkdown形式で作成してください。必要に応じて見出しやリスト、テーブルを活用し、情報を整理してください。ファイルとして保存してください。"
                )
            case OutputFormat.CSV:
                parts.append(
                    """【出力形式】
出力はCSV形式で作成してください。カラム名は上記データ項目に従い、各行のデータがカラムと正しく対応するようにしてください。カラム名は1行目に記載し、データは2行目以降に記載してください。ファイルとして保存してください。"""
                )
            case OutputFormat.TEXT:
                parts.append(
                    "【出力形式】\n出力はプレーンテキスト形式で作成してください。必要に応じて改行やインデントで情報を整理してください。ファイルとして保存してください。"
                )
            case _:
                parts.append(
                    f"【出力形式】\n{controller_type.value} 形式でファイルに保存してください。"
                )
    return "\n\n".join(parts)
