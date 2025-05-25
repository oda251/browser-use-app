from src.entity.controller_type import OutputFormat
from src.entity.agent_context import AgentContext
from src.entity.prompt_templates import (
    COMMON_INSTRUCTION_DEFAULT,
    OUTPUT_FORMAT_MARKDOWN,
    OUTPUT_FORMAT_MARKDOWN_RULE,
    OUTPUT_FORMAT_CSV,
    OUTPUT_FORMAT_CSV_RULE,
    OUTPUT_FORMAT_TEXT,
    OUTPUT_FORMAT_TEXT_RULE,
)


def compose_instruction(
    purpose: str,
    detail: str,
    reference_url: str | None,
    controller_type: OutputFormat | None,
    data_items: list[str] | None = None,
    common_instruction: str | None = None,
) -> tuple[str, str, AgentContext]:
    parts_main = []
    parts_context = []
    context = AgentContext()
    # 共通指示
    if common_instruction and common_instruction.strip():
        parts_main.append(f"[Common Instruction]\n{common_instruction.strip()}")
        parts_context.append(f"[Common Instruction]\n{common_instruction.strip()}")
    # 目的
    if purpose:
        parts_main.append(f"[Purpose]\n{purpose}")
        parts_context.append(f"[Purpose]\n{purpose}")
    # 詳細
    if detail:
        parts_main.append(f"[Detail]\n{detail}")
        parts_context.append(f"[Detail]\n{detail}")
    # 参考URL
    if reference_url:
        parts_main.append(f"[Reference URL]\n{reference_url}")
        parts_context.append(f"[Reference URL]\n{reference_url}")
    # データ項目
    filtered = [item for item in (data_items or []) if item.strip() != ""]
    if filtered:
        data_items_str = "[Data Items]\n- " + "\n- ".join(filtered)
        parts_main.append(data_items_str)
        parts_context.append(data_items_str)
    # 出力形式
    if controller_type:
        match controller_type:
            case OutputFormat.MARKDOWN:
                parts_main.append(OUTPUT_FORMAT_MARKDOWN)
                parts_context.append(OUTPUT_FORMAT_MARKDOWN_RULE)
            case OutputFormat.CSV:
                parts_main.append(OUTPUT_FORMAT_CSV)
                parts_context.append(OUTPUT_FORMAT_CSV_RULE)
            case OutputFormat.TEXT:
                parts_main.append(OUTPUT_FORMAT_TEXT)
                parts_context.append(OUTPUT_FORMAT_TEXT_RULE)
            case _:
                other_rule = f"[Output Format Rule]\nSave as a file in {controller_type.value} format."
                parts_main.append(
                    f"[Output Format]\nSave as a file in {controller_type.value} format."
                )
                parts_context.append(other_rule)
    return "\n\n".join(parts_main), "\n\n".join(parts_context), context
