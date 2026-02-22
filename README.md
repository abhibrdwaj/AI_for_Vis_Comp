# Automated Code Generation Pipeline

**From template to playable HTML5 maze game in one run.** This repository delivers an end-to-end **multi-agent AI pipeline** that automates game design, logic, UI/UX, asset generation, integration, and QA—emphasizing **performance**, **resilience**, and **reproducible automation** for AI-driven content creation.

---

## 1. Project Title & Hook

**AI for Visual Computing** demonstrates production-grade **LLM orchestration** for automated game development. A single kickoff turns a minimal HTML template and user preferences (platform, difficulty, features) into a complete, mobile-friendly maze game—with **resumable execution**, **rate-limit handling**, and **artifact-based context flow** between agents. The system is built for engineers who care about **low-friction automation** and **clear separation** between orchestration, configuration, and runtime.

---

## 2. Core Architecture & The Why

### Why This Architecture?

- **CrewAI + sequential process**  
  Game creation is a **dependency-ordered pipeline**: logic → UI → input → assets → integration → test. A **sequential** process with explicit `context` per task ensures each agent consumes only the artifacts it needs (e.g. `integrate_code_modules` sees `generate_game_logic`, `design_ui_ux`, `handle_input_controls`). This avoids non-determinism and keeps the pipeline interpretable and debuggable.

- **YAML-driven agents and tasks**  
  Roles, goals, backstories, models, and task graphs live in `config/agents.yaml` and `config/tasks.yaml`. **Why:** Experimentation and tuning happen in config and prompts—not in Python. Adding or swapping agents (e.g. a dedicated “narrative” agent) does not require refactoring the crew class; the codebase stays thin and maintainable.

- **Prompt files instead of inline strings**  
  Long instructions live in `prompts/*.txt` and are referenced via `prompt_file` in `agents.yaml`. **Why:** Version control, readability, and non-developer edits (e.g. product or design) without touching application code.

- **Single-file game output**  
  The code-integrator agent merges HTML, CSS, and JS into one deployable file (`final_game.html`). **Why:** Portability, offline play, and simple deployment (no build step or asset server). Aligns with the template’s design: one HTML file that can run anywhere.

- **Progress persistence and resumability**  
  After each task, progress is written to `game_outputs/progress.json` (`last_task`). On re-run, completed tasks are skipped and outputs are not overwritten. **Why:** Long runs (e.g. many image generations) survive interruptions and rate limits without redoing work.

- **No custom RAG/vector DB in this repo**  
  Context is passed **explicitly** via task `context` (prior task names) and shared `inputs` (e.g. `html_template`). CrewAI’s stack may pull in LangChain/Chroma as transitive dependencies; this project does not implement document ingestion or vector retrieval. The “retrieval” here is **structured artifact handoff** between steps—simpler and fully traceable.

---

## 3. Key Engineering Highlights

### ML / Data

- **LLM orchestration**  
  A **7-agent, 7-task** Crew runs sequentially: game logic → UI/UX → input controls → visual assets (DALL·E 3) → asset integration → code integration → test & debug. Each task declares dependencies via `context`; the framework injects prior outputs so agents operate on real artifacts.

- **Artifact ingestion and handoff**  
  The pipeline ingests the HTML template and user preferences at kickoff; each task’s output is written to `game_outputs/` (e.g. `script.js`, `ui_ux.html`, `input.js`, `code_integrated.html`, `final_game.html`). Downstream tasks consume these files through the crew’s context mechanism—no separate “retrieval” service, but a clear **data flow** from raw template to playable game.

- **Controlled use of tools**  
  Only the **image_asset_agent** uses a custom tool (`ImageGenerationTool`), which calls the OpenAI Images API (DALL·E 3, `b64_json`), writes PNGs under `game_outputs/images/`, and returns paths for the asset-integration agent. Keeps API surface small and behavior predictable.

### Software

- **Resilience and latency awareness**  
  `main.py` catches `litellm.RateLimitError`, parses “try again in Xs” when present, sleeps, and retries until `kickoff()` succeeds. Progress is saved after each task so partial runs can be resumed without re-executing completed steps.

- **Single-tenant, env-based secrets**  
  No multi-tenant logic; API keys are intended to come from environment (e.g. `.env`). The codebase uses placeholders in code for local runs; production usage should rely on `os.getenv("OPENAI_API_KEY")` and never commit secrets. `.gitignore` includes `.env`.

- **Test and quality bar**  
  A dedicated **tester_debugger_agent** validates the integrated game and produces the final artifact. The project is structured for **high testability**: config and prompts are decoupled so that adding unit/integration tests (e.g. pytest on crew outputs or template rendering) can target **90%+ coverage** of orchestration and file-generation logic without touching LLM calls.

---

## 4. Tech Stack

| Category        | Technologies |
|----------------|--------------|
| **Languages**  | Python 3.10–3.12, JavaScript (game logic/UI), HTML/CSS |
| **AI / ML**    | CrewAI (≥0.108.0, &lt;1.0.0) with `crewai[tools]`, LiteLLM, OpenAI (GPT models + DALL·E 3) |
| **Orchestration** | Sequential process; YAML-defined agents and tasks |
| **Tooling**    | UV (install/lock), Hatchling (build); prompt files in `prompts/*.txt` |
| **Output**     | Single-file HTML5 game; assets under `game_outputs/` |
| **Infrastructure** | Local execution; optional containerization (see Setup) |

---

## 5. Setup & Execution

### Prerequisites

- **Python** ≥3.10, &lt;3.13  
- **UV** for dependency management: `pip install uv`  
- **OpenAI API key** (for GPT and DALL·E); set in environment or `.env`

### Local Development (standard environment)

All commands below are from the **CREW_AI/game_version_v1/** directory (project root for the crew).

1. **Install UV** (if needed):
   ```bash
   pip install uv
   ```

2. **Install dependencies** (from `CREW_AI/game_version_v1/`):
   ```bash
   crewai install
   ```
   Or install via UV from the same directory:
   ```bash
   uv sync
   ```

3. **Configure secrets**  
   Create a `.env` in `CREW_AI/game_version_v1/` and add:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   Ensure the application reads this via `os.getenv("OPENAI_API_KEY")` in production; avoid hardcoding keys.

4. **Run the pipeline** (from `CREW_AI/game_version_v1/`):
   ```bash
   crewai run
   ```
   This kicks off the crew, writes artifacts to `game_outputs/`, and persists progress in `game_outputs/progress.json`. Open `game_outputs/final_game.html` in a browser to play the generated game.

### Optional: Docker

No Dockerfile is committed; you can wrap the same flow in a container, for example:

- Base image: `python:3.11-slim`
- Install UV, then `crewai install` (or `uv sync`) inside the project directory
- Set `OPENAI_API_KEY` via env at run time
- Run `crewai run` as the default command

---

## 6. Performance Metrics

| Metric | Target / Placeholder |
|--------|----------------------|
| **Pipeline latency** | Sub-minute to few minutes per full run (depends on LLM and image-generation calls). Resumable on failure or rate limit. |
| **Retrieval / handoff** | Artifact handoff between tasks is in-process and file-based; no network round-trips for “retrieval” within the pipeline. |
| **Automation efficiency** | End-to-end automation from template + preferences to playable game; placeholder: **~80%+ reduction** in manual game-assembly steps for this class of maze game. |
| **Resilience** | Automatic retry with backoff on rate limits; progress persistence avoids rework on partial runs. |
| **Test coverage (goal)** | Orchestration and file I/O designed for **90%+** unit/integration test coverage without invoking LLMs. |

---

## Repository Layout (Key Paths)

| Purpose | Path |
|--------|------|
| Crew definition (agents + tasks) | `CREW_AI/game_version_v1/src/game_version_v1/crew/GameVersionV1.py` |
| Entrypoint | `CREW_AI/game_version_v1/src/game_version_v1/main.py` |
| Agent config | `CREW_AI/game_version_v1/src/game_version_v1/config/agents.yaml` |
| Task config | `CREW_AI/game_version_v1/src/game_version_v1/config/tasks.yaml` |
| Image generation tool | `CREW_AI/game_version_v1/src/game_version_v1/tools/image_generation_tool.py` |
| Game template | `CREW_AI/game_version_v1/GameTemplate.html` |
| Generated game & progress | `CREW_AI/game_version_v1/game_outputs/` |
| Reference game (no AI) | `game_version0/index.html`, `game_version0/game_v3.html` |

---

*Built for the intersection of robust infrastructure and user experience—automation that is predictable, resumable, and easy to extend.*
