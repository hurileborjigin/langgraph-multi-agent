# Simple Stock Screener
A LangGraph-driven assistant that pairs an Azure OpenAI chat model with a yfinance-powered screener tool to surface curated Yahoo Finance results on demand.

## How It Works
- A user prompt enters a LangGraph flow backed by conversational memory.
- The chatbot node delegates finance questions to the `simple_screener` structured tool.
- The tool queries Yahoo Finance presets (for example, aggressive small caps) and returns a filtered JSON response that the model summarizes.

## Screenshots
- First request routed to the tool node  
  ![Screenshot 1](./Screenshot%202025-11-05%20at%2022.57.37.png)
- Follow-up request reuses conversation memory and hits the tool again  
  ![Screenshot 2](./Screenshot%202025-11-05%20at%2022.57.50.png)

## Prerequisites
- Python environment managed by `uv`
- Azure OpenAI credentials configured in `.env`
- Internet access to reach Yahoo Finance via `yfinance`

## Installation
```bash
uv sync
```

## Usage
1. Start the assistant:
   ```bash
   uv run flow.py
   ```
2. Ask for a screener, e.g. “Bring me a list of aggressive small cap stocks.”
3. Review the structured output printed to the terminal and in `stock-market/output.json`.
