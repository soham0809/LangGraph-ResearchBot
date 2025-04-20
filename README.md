# Dual-Agent AI Research System

A LangChain and LangGraph-based system featuring two specialized AI agents that work together to research and answer questions. This version requires no API keys and works completely offline.

## Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                                                                   │
│                          User Query                               │
│                              │                                    │
│                              ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                     LangGraph Workflow                     │   │
│  │                                                           │   │
│  │   ┌───────────────┐                ┌──────────────────┐   │   │
│  │   │ ResearchAgent │                │   AnswerAgent    │   │   │
│  │   │               │                │                  │   │   │
│  │   │ 1. DuckDuckGo │───Research────▶│ 1. Process      │   │   │
│  │   │    Search     │    Results     │    Results       │   │   │
│  │   │ 2. Process    │                │ 2. Generate      │   │   │
│  │   │    Content    │                │    Answer        │   │   │
│  │   │ 3. Summarize  │                │ 3. Add Citations │   │   │
│  │   └───────────────┘                └──────────────────┘   │   │
│  │                                             │             │   │
│  └─────────────────────────────────────────────┼─────────────┘   │
│                                                │                 │
│                                                ▼                 │
│                                      Formatted Answer            │
│                                      with Citations              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Features

- ResearchAgent: Uses DuckDuckGo to collect relevant information from the web
- AnswerAgent: Produces comprehensive, well-cited answers from research
- LangGraph Workflow: Orchestrates the agents in a unified state machine
- CLI Interface: Easy-to-use command line interface with rich formatting
- No API Keys Required: Uses local implementations for LLM functionality
- Error Handling: Robust error management throughout the workflow
- Structured Output: Well-formatted answers with proper source citations

## How It Works

This version of the system uses:

- DuckDuckGo Search: For web search (no API key required)
- Local LLM Simulation: For text generation (no API keys required)
- BeautifulSoup: For extracting content from web pages

## Requirements

- Python 3.8+
- No API keys required!

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/soham0809/LangGraph-ResearchBot.git

   cd LangGraph-ResearchBot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

To research a query:

```bash
python main.py "What are the latest advancements in quantum computing?"
```

To save the results to a file:

```bash
python main.py "What are the latest advancements in quantum computing?" --save results.md
```

## Example Output

```markdown
# Research: What are recent advances in quantum computing?

Based on the search results, here are the key findings:

1. Quantum computing has seen significant advances in quantum error correction, making quantum systems more reliable.

2. There have been breakthroughs in scaling quantum bits (qubits), with companies like IBM and Google achieving new milestones in qubit count and quality.

3. Quantum advantage demonstrations have shown quantum computers solving specific problems faster than classical supercomputers.

4. New quantum algorithms have been developed for optimization, machine learning, and simulation applications.

5. Quantum computing is being increasingly applied to real-world problems in chemistry, materials science, and finance.

## Sources

[1] Quantum computing | MIT News | Massachusetts Institute of Technology
URL: https://news.mit.edu/topic/quantum-computing

[2] The latest developments in quantum computing: A transformative frontier
URL: https://www.openaccessgovernment.org/article/latest-developments-quantum-computing/

[3] 2025 will see huge advances in quantum computing
URL: https://www.csiro.au/en/news/articles/2025-huge-advances-in-quantum-computing
```

## Module Structure

- `agents/`: Contains the agent implementations
  - `research_agent.py`: Web research agent using DuckDuckGo
  - `answer_agent.py`: Answer formatting agent
- `graph/`: Contains the LangGraph workflow
  - `agent_graph.py`: Defines the agent interaction graph
- `utils/`: Utility functions and configuration
  - `search.py`: Free web search utilities
  - `llm.py`: Local LLM implementation
- `cli.py`: Command-line interface
- `main.py`: Entry point

## License

MIT
