# 🤖 react-agent-loop

> A Python implementation of a **ReAct (Reasoning + Acting)** agent powered by GPT-4o, capable of solving multi-step problems by autonomously deciding when to search the web or perform calculations.

---

## 💡 How It Works

This agent follows the **ReAct pattern** — a loop where the model reasons about a problem, chooses a tool, observes the result, and repeats until it reaches a final answer.

```
User Question
     │
     ▼
┌─────────────────────────────┐
│  Thought: What should I do? │
│  Action: tool: "argument"   │  ◄── GPT-4o decides
│  PAUSE                      │
└────────────┬────────────────┘
             │
             ▼
     Tool is executed
             │
             ▼
┌─────────────────────────────┐
│  Observation: result        │  ◄── Injected back into context
└────────────┬────────────────┘
             │
      ┌──────┴──────┐
      │  Repeat or  │
      │  Answer     │
      └─────────────┘
```

---

## 🛠️ Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `pesquisar` | Searches Google via SerpAPI | `pesquisar: "preço do dólar 2026"` |
| `calcular` | Evaluates math expressions | `calcular: "1500 * 5.20"` |

New tools can be added to the `tools` dict and registered in the system prompt.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/massarrahelenna/react-agent-loop.git
cd react-agent-loop
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root of the project:
```env
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key
```

### 4. Run the agent
```bash
python agents.py
```

---

## 📦 Requirements

```
openai
google-search-results
python-dotenv
```

> See `requirements.txt` for pinned versions.

---

## 💬 Example Interaction

```
Welcome to react-agent-loop! Type your question or 'sair' to exit.

Digite sua pergunta: Qual o salário mínimo atual e quanto daria por mês trabalhando 220 horas?

Step 1:
Thought: I need to search for the current minimum wage in Brazil.
Action: pesquisar: "salário mínimo 2026 Brasil"
PAUSE

--- [Searching Google: salário mínimo 2026 Brasil] ---
Observation: O salário mínimo em 2026 é de R$ 1.518,00...

Step 2:
Thought: Now I can calculate the hourly rate for 220 hours.
Action: calcular: "1518 / 220"
PAUSE

Step 3:
Answer: The current minimum wage is R$ 1,518.00. Working 220 hours/month
gives an hourly rate of approximately R$ 6.90/hour.
```

---

## 🏗️ Project Structure

```
react-agent-loop/
├── agents.py          # Main agent loop
├── .requirements.txt  # Python dependencies
├── .gitignore
└── LICENSE            # MIT
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**massarrahelenna**  
Built as a study project on LLM agent architectures and the ReAct prompting pattern.
