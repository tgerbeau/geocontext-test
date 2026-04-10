# geocontext-test

This repository contains an integration test suite designed to validate the correct behavior of the MCP server `ignfab/geocontext` across different language models.

## Purpose

The main goal is to ensure that end-to-end interactions with `ignfab/geocontext` remain stable and consistent when switching model providers or model versions.

## What is tested

- Agent creation using a configured model name
- Real model invocation through integration scenarios
- Functional response checks for expected outputs

## Usage

### Testing with anthropic models

```bash
export MODEL_NAME="anthropic:claude-sonnet-4-6"
export ANTHROPIC_API_KEY=YourKey

uv run pytest
```

### Testing with google models

```bash
export MODEL_NAME="google_genai:gemini-2.5-flash"
export GOOGLE_API_KEY=YourKey

uv run pytest
```

```bash
export MODEL_NAME="google_genai:gemini-3.1-flash-lite-preview"
export GOOGLE_API_KEY=YourKey

uv run pytest
```

## Tests

- [test_france_capital.py](test_france_capital.py) - basic test without the MCP
- [test_chaining_geocode.py](test_chaining_geocode.py) - ensure that LLM can chain `geocode(str)->[lon,lat]` and `altitude(lon,lat) -> z`
- [test_search_batiment.py](test_search_batiment.py) - test search with "bâtiment" (*building*)
- [test_search_ecoles.py](test_search_ecoles.py) - test search with "écoles" (*schools*) - **UNSTABLE**

## License

[MIT](LICENSE)

