# 🔎 Multi-Agent Research System

An AI-powered research assistant that turns a single topic into a structured, reviewed research report. Four specialized stages work together: **search the web, read the best source, write a report, and critique it**, all behind a simple Streamlit interface.

Built with **LangChain**, **Google Gemini**, **Tavily**, and **Streamlit**.

---

## ✨ Features

- **Multi-agent pipeline**: separate agents for searching and reading, plus dedicated chains for writing and reviewing
- **Live web search** powered by Tavily
- **Web scraping** of the most relevant source with BeautifulSoup
- **Structured reports**: Introduction, Key Findings, Conclusion, and Sources
- **Critic review** with a score out of 10, strengths, areas to improve, and a one-line verdict
- **Streamlit UI** with a progress bar, run history, tabbed results, and Markdown report download
- **CLI mode** for running the pipeline straight from the terminal

---

## 🧠 How It Works

```
 Topic
   │
   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ 1. Search     │──▶│ 2. Reader     │──▶│ 3. Writer     │──▶│ 4. Critic     │
│    Agent      │   │    Agent      │   │    Chain      │   │    Chain      │
│ (Tavily)      │   │ (Scraper)     │   │ (Gemini)      │   │ (Gemini)      │
└───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘
   titles, URLs,       cleaned page        structured          score, strengths,
   snippets            text                report              improvements
```

| Stage | Type | Description |
|-------|------|-------------|
| **Search Agent** | LangChain agent + `web_search` tool | Queries the web and returns titles, URLs, and snippets |
| **Reader Agent** | LangChain agent + `scrape_url` tool | Picks the most relevant URL and scrapes deeper content |
| **Writer Chain** | Prompt → LLM → Output parser | Drafts a detailed report from the gathered research |
| **Critic Chain** | Prompt → LLM → Output parser | Reviews the report and returns a score with feedback |

---

## 🗂️ Project Structure

```
.
├── app.py               # Streamlit web interface
├── agent.py             # LLM setup, search/reader agents, writer & critic chains
├── pipeline.py          # Orchestrates the 4-step research pipeline
├── tools.py             # Tavily web search tool and web scraper tool
├── requirements.txt     # Python dependencies
└── .env                 # API keys (not committed)
```

---

## 🛠️ Tech Stack

- **Python 3.11+**
- [LangChain](https://www.langchain.com/) (agents, prompts, LCEL chains)
- [Google Gemini](https://ai.google.dev/) via `langchain-google-genai` (`gemini-2.5-flash-lite`)
- [Tavily](https://tavily.com/) for web search
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) + `requests` for scraping
- [Streamlit](https://streamlit.io/) for the UI

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API keys

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

- Get a Gemini key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Get a Tavily key from [tavily.com](https://tavily.com/)

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

---

## ▶️ Usage

### Web app (Streamlit)

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal, enter a topic (for example, *"Current advances in solid-state batteries"*), and click **Run**.

The results are organized into four tabs:

- **Report**: the final structured report
- **Critic Review**: score and feedback
- **Search Results**: what the search agent found
- **Scraped Content**: the text pulled from the chosen source

You can also download the report as a `.md` file and revisit earlier runs from the sidebar.

### Command line

```bash
python pipeline.py
```

You will be prompted for a topic, and each stage's output is printed to the terminal.

---

## 📄 Example Output

**Critic review format:**

```
Score: 8/10

Strengths:
- Clear structure and logical flow
- Well-supported key findings

Areas to Improve:
- Include more diverse sources
- Add more recent data points

One line verdict:
A solid, well-organized report that would benefit from broader sourcing.
```

---

## ⚙️ Configuration

You can tune the system by editing a few values:

| Setting | File | Default |
|---------|------|---------|
| LLM model | `agent.py` | `gemini-2.5-flash-lite` |
| Temperature | `agent.py` | `0` |
| Number of search results | `tools.py` | `2` |
| Scraped text length | `tools.py` | `2000` characters |

---

## 🔭 Future Improvements

- Scrape multiple sources instead of one
- Add a revision loop where the writer improves the report using the critic's feedback
- Export reports to PDF or DOCX
- Expose the pipeline as a REST API with FastAPI
- Add unit tests for the tools and pipeline

---

## ⚠️ Limitations

- The reader agent scrapes a single page, and some sites may block scraping or require JavaScript
- Report quality depends on the search results and the selected model
- AI-generated content can contain errors, so verify important facts using the listed sources

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to fork the repo and open a pull request.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Your Name**
GitHub: [prakashkumarsingh871-pks](https://github.com/prakashkumarsingh871-pks)

⭐ If you found this project useful, consider giving it a star!
