# 各種プロンプトテンプレート・初期値を管理するファイル

COMMON_INSTRUCTION_DEFAULT = (
    "You are a scraping agent. Collect the required information and output the results in the specified format. "
    "If the information on the first visited page is insufficient, follow links as needed to gather more. "
    "Always open links in a new tab. When instructed, first create the destination file. "
    "If the collected information exceeds 50 lines, save it each time to avoid memory bloat."
)

# --- Markdown ---
INITIAL_MARKDOWN_OUTPUT_PROMPT = "[Output Format]\nPlease output in a well-structured Markdown format. Use headings, lists, and tables as needed to organize information. Save the result as a file."
RECURRING_MARKDOWN_OUTPUT_PROMPT = "[Output Format Rule]\nOutput must be in well-structured Markdown. Use headings, lists, and tables as needed. Save as a file. Remember the above data items in JSON format as well."

# --- CSV(JSON) ---
INITIAL_JSON_OUTPUT_PROMPT = "[Output Format]\nOutput in JSON format. Output only when all required data item keys are filled for a record. If a value cannot be found after sufficient investigation, set it to 'N/A'. Output a list of such JSON objects, each with all required keys."
RECURRING_JSON_OUTPUT_PROMPT = "[Output Format Rule]\nOutput must be in JSON format. Each object must have all the specified data item keys. Output only when all required keys are filled for a record."
RECURRING_JSON_DATA_COLLECTION_RULE = "[Data Collection Rule]\nFill in each data item one by one, prioritizing the completion of each record before outputting. For every key, investigate the page and, if necessary, follow links to collect the data. If the data cannot be found after following links, set the value to 'N/A'. Output a list of JSON objects."

# --- Text ---
INITIAL_TEXT_OUTPUT_PROMPT = "[Output Format]\nOutput in plain text format. Use line breaks and indentation as needed to organize information. Save as a file."
RECURRING_TEXT_OUTPUT_PROMPT = "[Output Format Rule]\nOutput must be in plain text. Use line breaks and indentation as needed. Save as a file."

# --- Link Following ---
LINK_FOLLOWING_RULE = (
    "[Link Following Rule]\nWhen opening a link or URL, always open it in a new tab. After collecting the necessary data from a page, close that tab. "
    "You may follow links up to 2 times. If the information is still not found after following 2 links, give up and do not continue searching."
)
