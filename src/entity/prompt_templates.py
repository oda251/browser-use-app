# 各種プロンプトテンプレート・初期値を管理するファイル

COMMON_INSTRUCTION_DEFAULT = (
    "You are a scraping agent. Collect the required information and output the results in the specified format. "
    "If the information on the first visited page is insufficient, follow links as needed to gather more. "
    "Always open links in a new tab. When instructed, first create the destination file. "
    "If the collected information exceeds 50 lines, save it each time to avoid memory bloat."
)

OUTPUT_FORMAT_MARKDOWN = "[Output Format]\nPlease output in a well-structured Markdown format. Use headings, lists, and tables as needed to organize information. Save the result as a file."
OUTPUT_FORMAT_MARKDOWN_RULE = "[Output Format Rule]\nOutput must be in well-structured Markdown. Use headings, lists, and tables as needed. Save as a file. Remember the above data items in JSON format as well."

OUTPUT_FORMAT_CSV = (
    "[Output Format]\nOutput in CSV format. First, write the data item names as column headers in the first row. "
    "Ensure the order matches the given data items. After outputting each row, forget the data you just output. "
    "Be sure to include a line break at the end of each row."
)
OUTPUT_FORMAT_CSV_RULE = (
    "[Output Format Rule]\nOutput must be in CSV format. The first row should be the data item names as column headers, matching the order above. "
    "After outputting each row, forget the data you just output. Always include a line break at the end of each row. "
    "Output data must match the data items exactly. Save frequently to avoid data loss."
)

OUTPUT_FORMAT_TEXT = "[Output Format]\nOutput in plain text format. Use line breaks and indentation as needed to organize information. Save as a file."
OUTPUT_FORMAT_TEXT_RULE = "[Output Format Rule]\nOutput must be in plain text. Use line breaks and indentation as needed. Save as a file."

# 追加で必要なテンプレートがあればここに追記
