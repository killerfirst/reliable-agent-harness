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
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    model = os.getenv(
        "DEEPSEEK_MODEL",
        "deepseek-chat",
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": task,
        },
    ]

    for turn in range(1, 9):
        print(f"\n===== TURN {turn} =====")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )

        message = response.choices[0].message

        # 把模型这一轮产生的内容加入上下文
        messages.append(message)

        # 模型没有继续调用工具：
        # 当前 V0 直接相信它已经结束
        if not message.tool_calls:
            print("\n===== FINAL =====")
            print(message.content)

            return message.content

        for call in message.tool_calls:
            arguments = json.loads(call.function.arguments)

            print(f"\nTOOL: {call.function.name}")
            print(f"ARGS: {arguments}")

            result = execute_tool(
                call.function.name,
                arguments,
            )

            print(f"RESULT:\n{result[:2000]}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )

    raise RuntimeError(
        "Emergency stop: maximum turns reached"
    )
