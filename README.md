
# Evidence-First Equity Research Agent

An AI-powered research agent that generates concise, evidence-based equity research briefs from a local collection of Markdown documents. Built for an Indian equity research use case.

## Features

- Loads local Markdown documents and assigns stable source IDs.
- Uses an LLM through the AI Pipe OpenAI-compatible API.
- Generates a structured research brief with Snapshot, Bull case, Bear case, Open questions, and Sources.
- Includes source citations and reconstructs the source list from document metadata.
- Attempts to compress the brief to a maximum of 500 words.
- Validates required sections, citations, source-list entries, and word count.
- Includes tests for research-brief validation.

## Project structure

```text
.
├── prompts/
│   └── system_prompt.md
├── research_pack/
│   ├── README.md
│   └── *.md
├── src/
│   ├── agent.py
│   ├── ingest.py
│   └── validate.py
├── tests/
│   ├── test_validate.py
│   └── test_log.md
├── output/
│   └── research_brief.md
├── .env.example
├── .gitignore
├── pytest.ini
└── requirements.txt
```

## Requirements

- Python 3.12 or a compatible Python version supported by the dependencies.
- An AI Pipe API key and access to a compatible chat-completions model.
- Internet access for model API calls.

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

Edit `.env` and set the required values:

```dotenv
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://aipipe.org/openai/v1
OPENAI_MODEL=gpt-5-nano
```

Replace the example API key with your own key. Never commit `.env` or share its contents.

## Run the agent

Generate a brief for the example ticker:

```bash
python -m src.agent SRVCABLE
```

The generated brief is written to:

```text
output/research_brief.md
```

The ticker is a research label for the supplied test documents. The agent uses the local research pack and does not independently verify the company or retrieve live market data.

## Validate the output

Run the automated tests:

```bash
pytest -q
```

Run the validator's standalone demonstration:

```bash
python -m src.validate
```

The validator checks required sections, citation references, source-list entries, and the configured word limit. These checks do not establish that every factual claim or investment interpretation is correct.

## Research limitations

- The supplied research pack does not include the primary Q1 FY27 exchange filing. The generated brief must disclose this limitation.
- Conflicting reported figures should remain unresolved until supported by the appropriate primary evidence.
- Historical disclosures must be distinguished from current information.
- The agent is not a substitute for independent financial research and does not provide a verified valuation or personalized investment advice.

## Experiment log

Development iterations, validation failures, design changes, and final test results are recorded in `tests/test_log.md`.
