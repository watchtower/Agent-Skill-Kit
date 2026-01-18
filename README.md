# Agent Skill Kit (ASK)

![Agent Skill Kit Banner](assets/banner.png)

**Agent Skill Kit (ASK)** is a CLI toolkit for managing, distributing, and syncing skills across multiple AI agents. It serves as a unified "package manager" for your AI's capabilities, allowing you to define a skill once and deploy it to **Gemini, Claude, Codex, Antigravity, Cursor**, and more.

## 🧠 Why Agent Skill Kit?

Managing instructions for multiple AI agents is tedious. You often have to:
*   Copy `.cursorrules` to `.codex.md`.
*   Manually sync `~/instructions.md` with project-specific prompts.
*   Format skills differently for Gemini (`SKILL.md`) vs Claude (Slash Commands).

**ASK** solves this by treating skills as **reusable packages**.
1. **Define Once**: Write a skill in a standard format.
2. **Deploy Anywhere**: ASK transforms and copies the skill to the correct location and format for each agent.
3. **Sync**: Keep all your agents updated with a single command.

## 🚀 Features

- **Multi-Agent Support**: Native support for Gemini, Claude Code, OpenAI Codex, Antigravity, and Cursor.
- **Dynamic Discovery**: Automatically discovers available agents in the `agents/` directory.
- **Safe Copy**: Strictly adheres to "Do Not Overwrite". Prompts for a new name if a skill conflicts.
- **Local & Global**: Choose between **Project-Local** (specific to one repo) or **Global** (user-wide) deployment.
- **AI-Assisted Creation**: Includes meta-skills that teach your AI how to create new skills (`skill-creator`) or add new agents (`add-agent`).
- **Extensible**: Add support for any new AI agent in seconds via the `ask add-agent` wizard.

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/NavanithanS/Agent-Skill-Kit.git
cd Agent-Skill-Kit

# Install in editable mode
pip install -e .
```

## 🛠 Usage

### 1. Copy Skills to an Agent ⭐
**The primary way to use ASK** — Deploy skills to your AI agents using the interactive wizard.

**Interactive Mode** (Recommended):
```bash
ask copy
```
The wizard guides you through:
1. **Skill Selection**: Beautiful table showing all skills with descriptions and categories
2. **Agent Selection**: Compatible agents highlighted for your chosen skill
3. **Destination**: Choose between local (project) or global (user-wide) installation

**Quick Mode** (with flags):
```bash
# Copy specific skill
ask copy gemini --skill bug-finder

# Copy all compatible skills to an agent
ask copy claude --all
```

### 2. List Available Skills
View your library of skills, including descriptions and supported agents.
```bash
ask list
```

### 3. Create a New Skill
**AI-Assisted** (Recommended):
Simply ask your AI agent to create a skill for you:
```
"Create a new skill for Docker best practices"
"Make a skill that teaches REST API design"
```
*Prerequisites: Deploy `ask-skill-creator` to your agent first (see [Available Skills](#-available-skills)).*

**Manual CLI** (Alternative):
Launch the interactive wizard to generate a standardized skill template.
```bash
ask create skill
```

### 4. Sync All Skills
Synchronize your entire skill library to all supported agents at once.
```bash
ask sync all
```

### 5. Add Support for New Agents
Want to use **Windsurf** or **Aider**? Use the scaffold wizard:
```bash
ask add-agent
```
This creates the necessary adapter code, making the new agent available instantly.

## 🎯 Supported Agents

| Agent | Local Path (Project) | Global Path (User) | Format |
|-------|----------------------|--------------------|--------|
| **Antigravity** | `.agent/skills/` | `~/.gemini/antigravity/skills/` | SKILL.md (YAML) |
| **Gemini CLI** | `.gemini/skills/` | `~/.gemini/skills/` | SKILL.md (YAML) |
| **Claude Code** | `.claude/commands/` | `~/.claude/commands/` | Markdown Command |
| **Codex** | `codex.md` | `~/.codex/instructions/` | Markdown |
| **Cursor** | `.cursor/rules/` | `~/.cursor/rules/` | Markdown Rules |

## � Available Skills

ASK comes with a curated collection of skills to boost your AI agent's capabilities. Each skill provides specialized instructions and best practices.

### Coding Skills

#### 🐛 ask-bug-finder
**Description**: Best practices for systematic bug hunting and debugging

**How to Use**:
```bash
# Deploy to all agents
ask copy --skill ask-bug-finder --all

# Deploy to specific agent
ask copy gemini --skill ask-bug-finder
```

**Use Cases**:
- Systematic debugging of complex issues
- Reproducing and isolating bugs
- Using debugging tools effectively (debuggers, loggers, profilers)
- Avoiding common bug patterns (off-by-one errors, null references, race conditions)
- Binary search debugging and git bisect workflows

---

#### 🔄 ask-python-refactor
**Description**: Best practices and guidelines for Python code refactoring

**How to Use**:
```bash
ask copy antigravity --skill ask-python-refactor
```

**Use Cases**:
- Improving Python code quality and maintainability
- Applying clean code principles to Python projects
- Refactoring legacy Python code
- Following Python-specific best practices and idioms

---

#### ✅ ask-commit-assistance
**Description**: Assist with code review, staging, and committing changes

**How to Use**:
```bash
# Make this available to your preferred agent
ask copy cursor --skill ask-commit-assistance
```

**Use Cases**:
- Automated code review before commits
- Generating meaningful commit messages (short and long formats)
- Staging files systematically
- Ensuring code quality before version control
- Creating professional commit messages following best practices

---

#### 🔍 code-reviewer
**Description**: An AI code reviewer that provides constructive feedback on code changes

**How to Use**:
```bash
ask copy --skill code-reviewer --all
```

**Use Cases**:
- Getting feedback on code quality, security, and performance
- Identifying potential bugs and anti-patterns
- Ensuring code follows best practices
- Pre-commit code quality checks
- Learning from constructive code review feedback

---

### Tooling Skills (Meta-Skills)

#### 🛠️ ask-skill-creator
**Description**: Teaches AI agents how to create skills for Agent Skill Kit

**How to Use**:
```bash
# Deploy to all agents so they can create skills
ask sync all
```

**Use Cases**:
- **AI-Assisted Skill Creation**: Let your AI agent create new skills by simply asking
  ```
  "Create a skill for API design best practices"
  ```
- Standardizing skill structure and format
- Automating skill scaffolding
- Building your custom skill library
- Teaching AI agents the skill creation workflow

**Example Workflow**:
1. Deploy this skill to your agent: `ask copy gemini --skill ask-skill-creator`
2. Ask your agent: "Create a skill called 'docker-best-practices' for containerization guidelines"
3. The agent generates the skill files automatically

---

#### 🎯 ask-add-agent
**Description**: How to add support for new AI code editors to Agent Skill Kit

**How to Use**:
```bash
# Deploy to help your agent add new editor support
ask copy antigravity --skill ask-add-agent
```

**Use Cases**:
- **Extending ASK**: Add support for new AI editors (Windsurf, Aider, etc.)
- Creating custom agent adapters
- Understanding the agent adapter architecture
- Contributing new agent support to the project

**Example Workflow**:
1. Deploy this skill to your agent
2. Run the wizard: `ask add-agent`
3. Or ask your agent to help: "Add support for Windsurf editor"
4. The agent follows the documented process to create the adapter

---

### 🚀 Quick Start with Skills

```bash
# View all available skills
ask list

# Deploy a specific skill to an agent
ask copy gemini --skill ask-bug-finder

# Deploy all compatible skills to an agent
ask copy claude --all

# Sync all skills to all agents
ask sync all

# Create your own skill (interactive)
ask create skill

# Or ask your AI agent to create one (if skill-creator is deployed)
"Create a new skill for API testing best practices"
```

## �📐 Skill Format

Each skill is a directory containing:
*   **`skill.yaml`**: Metadata (name, description, tags, supported agents).
*   **`README.md`**: The actual prompt/instructions for the AI.

> [!IMPORTANT]
> **Naming Convention**: All skill names must start with the `ask-` prefix (e.g., `ask-bug-finder`, `ask-commit-assistance`).

```yaml
# skill.yaml
name: ask-bug-finder
version: 1.0.0
category: coding
agents:
  - gemini
  - claude
  - cursor
```

## 🧩 Design Principles

1.  **Universal Definition**: Skills are defined in a neutral format that can be adapted to any agent.
2.  **Local-First, Global-Ready**: Prioritize project-specific skills (checked into git) while supporting user-wide global skills.
3.  **Safe by Default**: The CLI will **never** silently overwrite an existing skill. It always asks.
4.  **Agentic Workflow**: The toolkit includes skills (`skill-creator`) specifically designed to help AI agents help *you* build more skills.

## 🗂 Repository Structure

```
agent-skill-kit/
├── ask/                     # CLI Source Code
│   ├── commands/            # logic for create, copy, sync, add-agent
│   └── utils/               # adapter logic, filesystem helpers
├── agents/                  # Adapters for each AI agent
│   ├── gemini/
│   ├── claude/
│   ├── codex/
│   ├── antigravity/
│   └── cursor/              # (Added via ask add-agent)
└── skills/                  # The Skill Library
    ├── coding/
    └── tooling/
```

## 🤝 Contributing

Contributions are welcome!
1.  **Create a Skill**: Use `ask create skill` and submit a PR with your best prompts.
2.  **Add an Agent**: Use `ask add-agent`, test it, and submit the new adapter.

## License

MIT
