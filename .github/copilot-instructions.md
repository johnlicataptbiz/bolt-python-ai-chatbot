<!-- .github/copilot-instructions.md: Guidance for AI coding agents working on this repo -->
# Copilot / AI Agent Instructions — bolt-python-ai-chatbot

Purpose: give an AI coding agent the exact, actionable knowledge needed to be productive in this repository.

- **Quick start (what humans run locally):**
  - `python3 -m venv .venv && source .venv/bin/activate`
  - `pip install -r requirements.txt`
  - Set required env vars: `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`. Provider keys used in this repo: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `VERTEX_AI_PROJECT_ID`, `VERTEX_AI_LOCATION`.
  - Run the app: `python3 app.py`
  - Lint/format: `ruff check .` and `ruff format .`

- **High-level architecture (read across these files):**
  - `app.py`: app entrypoint and request routing.
  - `listeners/`: organized by Slack surface — `commands/`, `events/`, `functions/`. Add listeners here for new Slack interactions.
  - `ai/`: core AI integrations.
    - `ai/ai_constants.py` contains project-wide AI constants.
    - `ai/providers/base_provider.py` defines the provider interface to implement.
    - `ai/providers/*.py` contains provider adapters (OpenAI, Anthropic, Vertex). Update `ai/providers/__init__.py` to expose/register a new provider.
  - `state_store/` + `data/`: application-level state. `state_store/file_state_store.py` (FileStateStore) persists a per-user JSON file under `data/` holding user selection (`user_id`, `provider`, `model`). Use `get_user_state.py` and `set_user_state.py` for reading/writing.
  - `manifest.json`: Slack app declaration — update this and the Slack dashboard together when adding scopes/commands.
  - `app_oauth.py`: OAuth helper (used when distributing the app). For local testing use ngrok and `slack/oauth_redirect` as described in `README.md`.

- **Common, repo-specific patterns you must follow:**
  - Providers implement the `BaseProvider`-style interface in `ai/providers/base_provider.py` and are exposed via `ai/providers/__init__.py` helper utilities. When adding a provider: create `ai/providers/your_provider.py`, implement the interface, then import/register it in `ai/providers/__init__.py`.
  - Listener files are grouped by Slack surface. Put new command handlers in `listeners/commands/`, event handlers in `listeners/events/`, and workflow/functions in `listeners/functions/`.
  - Persistent user settings live as per-user JSON files in `data/`. Read/write via `state_store/file_state_store.py`. The user object uses the `UserIdentity` class from `state_store/user_identity.py` (fields: `user_id`, `provider`, `model`).

- **Integration points / external dependencies to be careful with:**
  - External model APIs: OpenAI, Anthropic, Vertex. Requests go through classes in `ai/providers/` — do not hardcode keys; use env vars listed above.
  - Slack platform: updating `manifest.json` alone is not sufficient — the Slack App config and installed workspace must be kept in sync.
  - File-based state: tests and local runs will create files under `data/`. Be careful when modifying `file_state_store.py` as it affects persisted user preferences.

- **Developer workflow & debugging tips (project-specific):**
  - Recreate environment: `python3 -m venv .venv` -> `source .venv/bin/activate` -> `pip install -r requirements.txt`.
  - Start server: `python3 app.py`. Use ngrok for external endpoints: `ngrok http 3000` and add redirect URL to Slack if using OAuth.
  - Logs: the app uses standard console logging — inspect runtime output for handler entry/exit; use Slack's request inspector for incoming event details.
  - Linting: `ruff check .` and `ruff format .` are the canonical formatting/lint commands in this repo.

- **Where to change things for common tasks (examples):**
  - Add a new slash command: add handler under `listeners/commands/`, then update `manifest.json` (and re-install the app in Slack if needed).
  - Add a new LLM provider: add `ai/providers/new_provider.py` implementing `BaseProvider`, then import and expose it in `ai/providers/__init__.py`.
  - Change how user preferences are stored: modify `state_store/file_state_store.py` and update `get_user_state.py` / `set_user_state.py` callers.

- **Safety and scope rules for automated edits:**
  - Do not change `manifest.json` without also updating the Slack App configuration or documenting required manual steps for re-installation.
  - Avoid altering `data/` files programmatically in a way that breaks backward compatibility; preserve the per-user JSON shape (`user_id`, `provider`, `model`).
  - For any change that affects provider credentials or request patterns, add a short note in `README.md` and ensure environment variable names match those read by the code.

- **Files to read first when landing in this repo:**
  - `README.md` — how to run locally and env var list.
  - `app.py` — routing and entrypoint.
  - `listeners/` — existing handlers to copy patterns from.
  - `ai/providers/base_provider.py` and `ai/providers/__init__.py` — provider interface and registration.
  - `state_store/file_state_store.py` and `state_store/user_identity.py` — how user settings are persisted.

If anything in this file is unclear or you need examples expanded (for instance a sample provider skeleton or a listener template), say which section to expand and I will iterate.
