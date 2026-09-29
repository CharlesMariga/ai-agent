# AI Agent

A small AI coding agent for the terminal, written in Python. You give it a prompt, and it works toward an answer by calling tools (listing files, reading them, writing them, running Python) in a loop until it has a final response.

It talks to models through [OpenRouter](https://openrouter.ai) using the OpenAI SDK. Built while following the [Boot.dev](https://www.boot.dev) "Build an AI Agent in Python" course.

> [!WARNING]
> This is a learning project, not a production tool. The agent can write files and execute Python code on your machine. It is confined to the `calculator/` directory by path checks only, with no real sandboxing, so don't point it at anything you care about.

## How it works

1. Your prompt is sent to the model along with a system prompt and the schemas of the available tools.
2. The model either answers in plain text or asks for one or more tool calls.
3. Tool calls are executed locally and their results are appended to the conversation.
4. Steps 2 and 3 repeat until the model gives a final answer, up to a limit of 20 iterations.

## Tools

| Tool | What it does |
| --- | --- |
| `get_files_info` | Lists the files in a directory with their size and whether they are directories |
| `get_file_content` | Reads a file, truncated at 10,000 characters |
| `run_python_file` | Runs a Python file with optional arguments and returns its stdout and stderr (30 second timeout) |
| `write_file` | Creates or overwrites a file, creating parent directories as needed |

Every tool takes paths relative to the working directory, which is injected by the agent rather than chosen by the model. Paths that resolve outside of it are rejected.

## Setup

Requirements:

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- An [OpenRouter API key](https://openrouter.ai/keys)

```sh
git clone https://github.com/CharlesMariga/ai-agent.git
cd ai-agent
uv sync
cp .env.example .env
```

Then open `.env` and set `OPENROUTER_API_KEY` to your own key.

## Usage

```sh
uv run main.py "<prompt>" [--verbose]
```

Examples:

```sh
uv run main.py "What files are in the root directory?"
uv run main.py "Read main.py and explain how the calculator renders its output"
uv run main.py "Run the calculator tests and tell me if they pass" --verbose
```

`--verbose` also prints the prompt, token usage, the arguments of each tool call, and each tool result.

## Configuration

There are no config files beyond `.env`. The other settings are constants in the code:

| Setting | Where | Default |
| --- | --- | --- |
| Model | `main.py` | `openrouter/free` |
| Iteration limit | `main.py` | `20` |
| Working directory | `call_function.py` | `./calculator` |
| File read limit | `config.py` | `10000` characters |
| System prompt | `prompts.py` | |

## Project structure

```
.
├── main.py              # CLI entry point and agent loop
├── call_function.py     # Tool registry and dispatcher
├── prompts.py           # System prompt
├── config.py            # Constants
├── functions/           # Tool implementations and their schemas
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
├── calculator/          # Sample project the agent works on
└── test_*.py            # Manual test scripts for each tool
```

## Testing

The `test_*.py` files in the root are print-based scripts that exercise each tool against the `calculator/` directory, including paths that should be rejected:

```sh
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_run_python_file.py
uv run test_write_file.py
```

The sample calculator has its own unit tests:

```sh
cd calculator
uv run tests.py
```
