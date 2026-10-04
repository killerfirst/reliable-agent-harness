import json
import os

from openai import OpenAI

from harness.registry import TOOL_SCHEMAS, execute_tool


SYSTEM_PROMPT = """
You are a coding agent working inside a restricted workspace.

Your job is to solve the user's coding task.

Rules:
- Inspect files before modifying them.
- Use only the tools provided.
- Do not assume a modification works.
- Run tests before claiming the task is complete.
- Do not modify test files unless explicitly requested.
"""


def run_agent(task: str) -> str:
    client = OpenAI()

    model = os.getenv(
        "OPENAI_MODEL",
        "gpt-5.6-terra",
    )

    inputs = [
        {
            "role": "user",
            "content": task,
        }
    ]

    for turn in range(1, 9):
        print(f"\n===== TURN {turn} =====")

        response = client.responses.create(
            model=model,
            instructions=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            input=inputs,
        )

        # 把模型这一轮产生的内容加入上下文
        inputs += response.output

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # 模型没有继续调用工具：
        # 当前 V0 直接相信它已经结束
        if not tool_calls:
            print("\n===== FINAL =====")
            print(response.output_text)

            return response.output_text

        for call in tool_calls:
            arguments = json.loads(call.arguments)

            print(f"\nTOOL: {call.name}")
            print(f"ARGS: {arguments}")

            result = execute_tool(
                call.name,
                arguments,
            )

            print(f"RESULT:\n{result[:2000]}")

            inputs.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": result,
                }
            )

    raise RuntimeError(
        "Emergency stop: maximum turns reached"
    )
