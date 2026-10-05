import asyncio
import json
import os
from pathlib import Path

import ollama
import mcp.types as types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

MCP_DIR = Path(__file__).resolve().parent

API_BASE_URL = os.getenv(
    "LUXURY_WATCH_API_BASE_URL",
    "https://api.dcanguven.workers.dev",
)


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"{name} environment variable is required."
        )

    return value


def build_ollama_tools(
    mcp_tools: list,
) -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.input_schema,
            },
        }
        for tool in mcp_tools
    ]


def format_tool_result(
    result,
) -> str:
    if result.structured_content is not None:
        return json.dumps(
            result.structured_content,
            ensure_ascii=False,
        )

    parts = []

    for item in result.content:
        if isinstance(
            item,
            types.TextContent,
        ):
            parts.append(item.text)
        else:
            parts.append(
                json.dumps(
                    item.model_dump(
                        mode="json",
                    ),
                    ensure_ascii=False,
                )
            )

    return "\n".join(parts)


async def main() -> None:
    api_key = get_required_env(
        "LUXURY_WATCH_API_KEY"
    )
    model = get_required_env(
        "OLLAMA_MODEL"
    )

    server_params = StdioServerParameters(
        command="uv",
        args=[
            "run",
            "python",
            "server.py",
        ],
        cwd=MCP_DIR,
        env={
            "LUXURY_WATCH_API_KEY": api_key,
            "LUXURY_WATCH_API_BASE_URL": API_BASE_URL,
        },
    )

    async with stdio_client(
        server_params
    ) as (
        read,
        write,
    ):
        async with ClientSession(
            read,
            write,
        ) as session:
            await session.initialize()

            tools_response = (
                await session.list_tools()
            )

            tools = build_ollama_tools(
                tools_response.tools
            )

            client = ollama.AsyncClient()

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a luxury watch market data assistant. "
                        "Use the available tools for questions about "
                        "watch brands, models, prices, records, and details. "
                        "Base market data answers on tool results. "
                        "Do not invent market data."
                    ),
                }
            ]

            print(
                f"Luxury Watch MCP Agent ({model})"
            )

            print(
                "Available tools: "
                + ", ".join(
                    tool.name
                    for tool in tools_response.tools
                )
            )

            print("Type 'exit' to quit.")

            while True:
                prompt = input(
                    "\nYou: "
                ).strip()

                if prompt.lower() in {
                    "exit",
                    "quit",
                }:
                    break

                if not prompt:
                    continue

                messages.append(
                    {
                        "role": "user",
                        "content": prompt,
                    }
                )

                while True:
                    response = (
                        await client.chat(
                            model=model,
                            messages=messages,
                            tools=tools,
                        )
                    )

                    messages.append(
                        response.message
                    )

                    tool_calls = (
                        response.message.tool_calls
                    )

                    if not tool_calls:
                        print(
                            "\nAssistant: "
                            + response.message.content
                        )
                        break

                    for tool_call in tool_calls:
                        name = (
                            tool_call.function.name
                        )

                        arguments = dict(
                            tool_call.function.arguments
                        )

                        print(
                            f"\nTool: {name}"
                        )

                        print(
                            "Arguments: "
                            + json.dumps(
                                arguments,
                                ensure_ascii=False,
                            )
                        )

                        result = (
                            await session.call_tool(
                                name,
                                arguments=arguments,
                            )
                        )

                        messages.append(
                            {
                                "role": "tool",
                                "tool_name": name,
                                "content": (
                                    format_tool_result(
                                        result
                                    )
                                ),
                            }
                        )


if __name__ == "__main__":
    asyncio.run(main())