import json

from harness.tools import (
    list_files,
    read_file,
    replace_text,
    run_tests,
)


TOOL_SCHEMAS = [
    {
        "type": "function",
        "name": "list_files",
        "description": "List files available in the workspace.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "read_file",
        "description": "Read a UTF-8 text file from the workspace.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path relative to the workspace.",
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "replace_text",
        "description": (
            "Replace exactly one occurrence of old text "
            "inside a workspace file."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "old": {"type": "string"},
                "new": {"type": "string"},
            },
            "required": ["path", "old", "new"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "run_tests",
        "description": "Run pytest inside the workspace.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


TOOL_HANDLERS = {
    "list_files": list_files,
    "read_file": read_file,
    "replace_text": replace_text,
    "run_tests": run_tests,
}


def execute_tool(name: str, arguments: dict) -> str:
    if name not in TOOL_HANDLERS:
        return json.dumps(
            {
                "ok": False,
                "error": f"Unknown tool: {name}",
            }
        )

    try:
        result = TOOL_HANDLERS[name](**arguments)

        return json.dumps(
            {
                "ok": True,
                "result": result,
            },
            ensure_ascii=False,
        )

    except Exception as exc:
        return json.dumps(
            {
                "ok": False,
                "error": str(exc),
            },
            ensure_ascii=False,
        )
    