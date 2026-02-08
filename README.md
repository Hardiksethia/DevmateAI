# DevmateAI 🤖⚙️  
### An Autonomous AI-Powered Developer CLI Agent

DevmateAI is an AI-driven command-line developer assistant that understands natural language instructions and safely converts them into **validated, multi-step execution plans** to modify codebases, interact with Git, GitHub, and reason over repositories.

Unlike chat-based coding assistants, DevmateAI is built as a **real agent system** with strict planning, execution boundaries, safety guarantees, and full test coverage—designed for real-world developer workflows.

---

## 🎯 Overview

DevmateAI enables developers to work faster by delegating routine and complex engineering tasks directly from the terminal.

With DevmateAI, you can:

- Add or modify real source code files via natural language
- Explain and analyze existing code using repository-aware context
- Run Git operations (status, diff, commit)
- Interact with GitHub (list PRs, fetch PR comments)
- Automatically plan multi-step developer workflows
- Maintain strict safety and validation guarantees

---

## ✨ Key Features

### 🧠 LLM-Powered Planning Engine
- Converts user intent into **strict JSON execution plans**
- Enforces allow-listed actions only
- Rejects unsafe or ambiguous instructions
- Fully deterministic execution after planning

### 📁 Repository-Aware Reasoning (RAG-lite)
- Dynamically scans repository structure
- Uses LLM-based context selection to read only relevant files
- Injects repository context into planning prompts
- Enables accurate code explanations and modifications

### ⚙️ Deterministic Execution Engine
- Each action maps to a predefined executor handler
- No arbitrary shell execution
- Strong validation of payloads and arguments
- Safe filesystem, Git, and GitHub tooling

### 🧩 Modular Agent Architecture
- Planner, Executor, and Tools are fully decoupled
- Easy to extend with new actions and integrations
- Testable and mockable at every layer

### 🧪 Production-Grade Testing
- Full unit test coverage
- LLM calls fully mocked
- Git and GitHub interactions mocked
- Ensures reliability and safety

---

## 🏗️ Architecture

CLI (Typer)
│
▼
Agent
│
├── Planner (LLM → JSON Plan)
│ ├── Context Selector (LLM)
│ └── Plan Validator
│
└── Executor (Deterministic)
├── Filesystem Tools
├── Git Tools
└── GitHub Tools


Execution Flow: User Intent → Plan → Validate → Execute → Results

Execution Flow
User Intent
   ↓
Planner (LLM)
   ↓
[
  github_get_pr_review_comments,
  read_file,
  write_file,
  git_commit
]
   ↓
Executor (Deterministic)
   ↓
Updated Code + Commit



---

## 🛠️ Tech Stack

### Core
- **Python 3.10+**
- **Typer** – CLI framework
- **Rich** – Structured terminal output
- **dotenv** – Environment configuration

### AI / LLM
- **OpenAI API** (GPT-4o / GPT-4o-mini)
- Strict JSON-only prompting
- Deterministic execution after planning

### Developer Tooling
- **Git CLI**
- **PyGithub** – GitHub API integration
- **Pathlib** – Safe filesystem operations

### Testing
- `unittest`
- `unittest.mock`
- Full isolation of external dependencies

---

## 📁 Project Structure

devmate/
├── devmate/
│ ├── cli.py # CLI entrypoint
│ ├── config.py # Environment & settings
│ ├── logger.py # Structured logging
│ │
│ ├── core/
│ │ ├── agent.py # Orchestrator
│ │ ├── planner.py # LLM-powered planner
│ │ ├── executor.py # Action executor
│ │ ├── llm_client.py # OpenAI client wrapper
│ │ └── context.py # Repo context builder
│ │
│ └── tools/
│ ├── filesystem.py # Read/write/list files
│ ├── git.py # Git operations
│ └── github.py # GitHub API tools
│
├── tests/ # Unit tests
├── requirements.txt
├── .env
├── .gitignore
└── README.md



---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Git
- OpenAI API key
- (Optional) GitHub token for GitHub automation

---

### Installation

```bash
git clone https://github.com/yourusername/devmate.git
cd devmate

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

Health Check
python -m devmate run "health"


Explain Existing Code
python -m devmate run "explain how git commits are handled"

Modify or Add Code
python -m devmate run "add a utility function add(a, b) in devmate/tools/math.py"

Git Operations
python -m devmate run "check git status"
python -m devmate run "show git diff"


GitHub Automation
python -m devmate run "list open prs in owner/repo"


🔒 Safety Model

DevmateAI enforces strict safety boundaries:
Only explicitly allowed actions can execute
All plans are validated before execution
No arbitrary shell access
File operations restricted to repository
GitHub actions require explicit tokens
This design prevents uncontrolled LLM behavior while preserving autonomy.


Testing

Run all tests:
python -m unittest discover tests

Test coverage includes:

Planner validation

Context selection

Executor actions

Agent orchestration

Git and GitHub tooling

LLM behavior (mocked)



Future Roadmap:

Diff-based patch application (instead of overwrite)

Test-aware code changes

PR review comment auto-fix

Approval gates for destructive actions

Plugin system for custom tools

Long-term repository memory






New Feature: Auto-Fix GitHub PR Review Comments 🤖🔧
DevmateAI can now automatically fix GitHub Pull Request review comments by analyzing reviewer feedback, modifying the relevant code, and committing the fixes — all from a single natural language command.
This brings DevmateAI closer to a true autonomous code-review agent.


What the Auto-Fix PR Feature Does
When a user runs:
python -m devmate run "fix review comments for PR 12 in owner/repo"

DevmateAI will:
Fetch all review comments for the given PR
Identify:
File paths
Commented lines
Reviewer feedback text
Read the relevant source files
Use the LLM to:
Understand the reviewer’s intent
Propose safe, minimal fixes
Apply code changes deterministically
Commit the fixes with a clear commit message


Why DevmateAI?
DevmateAI demonstrates:
Real-world AI agent architecture
Safe and testable LLM integration
Deterministic execution with autonomy
Deep integration with developer tooling
This project is intentionally designed to reflect production-grade AI agent systems used in modern developer platforms.


👤 Author
Hardik Sethia
Building AI agents, developer tools, and autonomous systems.







