import json, re, logging

# The Bright Data MCP server sends some progress notifications the newest
# client validates strictly; failures there are already caught and logged
# internally, they never crash your code. This remove that noise.
logging.getLogger("client").setLevel(logging.ERROR)

WRAPPER_PATTERN = re.compile(
    r"=====UNTRUSTED_[a-f0-9]+_BEGIN=====\s*(.*?)\s*=====UNTRUSTED_[a-f0-9]+_END=====",
    re.DOTALL
)

def strip_security_wrapper(text):
    """Bright Data MCP wraps fetched web content in a tamper-evident marker
    to flag it as untrusted (prompt-injection defense). Strip it to get the
    raw payload underneath."""
    match = WRAPPER_PATTERN.search(text)
    return match.group(1) if match else text

def get_data(result):
    """Return a tool result's payload as a Python object.

    v2's CallToolResult exposes:
      - result.structured_content : parsed JSON, IF the tool declares an
        output schema
      - result.content : a list of content blocks (TextContent, etc.) —
        the fallback for tools that only return text/JSON-as-text
      - result.is_error : True if the tool call itself failed
    """
    if result.is_error:
        for block in result.content:
            if hasattr(block, "text"):
                print("TOOL ERROR:", block.text)
        return None

    if result.structured_content:
        return result.structured_content

    for block in result.content:
        if hasattr(block, "text") and block.text:
            text = strip_security_wrapper(block.text)
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text
    return None