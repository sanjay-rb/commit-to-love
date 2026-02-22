### Project Guidelines

## Code Style
- Language: `Python 3.12` (CI uses 3.12.3). Follow existing file style in `main.py` (PEP8-friendly, no one-letter variables).
- Formatting: No auto-formatter enforced; preserve existing simple layout and logging format when editing `main.py`.

## Architecture
- Core flow: `prompt.txt` → LLM (`openrouter/free`) → split on literal `Answer:` → send riddle, wait 30s, send answer (see `main.py`).
- Deployment: Scheduled GitHub Action in `.github/workflows/love.yml` decodes `secrets.DOT_ENV` → runs `pylint` → `python main.py` (daily cron at 4:30 UTC).

## Build and Test
- Install deps: `pip install -r requirements.txt` (see `requirements.txt`).
- Local run: create a `.env` with `OPEN_ROUTER_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, then `python main.py`.
- CI commands (mirrored in workflow):
	- `python -m pip install --upgrade pip` then `pip install -r requirements.txt`
	- `pylint main.py` (pre-flight lint)
	- `python main.py` (execution)

## Project Conventions
- Prompts: Keep prompts in `prompt.txt` and interpolate `{DATE}` using `.format(DATE=...)` (example: `main.py`).
- Output parsing: Code splits on the literal string `Answer:` to separate riddle and answer—ensure edits preserve that contract or add robust validation.
- UX timing: The `time.sleep(30)` delay is intentional and should not be removed without explicit instruction.
- Personalization: Header/footer lists live in `main.py` (e.g., `riddle_headers`) and are sampled at send-time.

## Integration Points
- OpenRouter: `OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPEN_ROUTER_API_KEY"))` and `TEXT_GENERATION_MODEL = "openrouter/free"` (see `main.py`).
- Telegram: Uses Bot API via `https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage` with `parse_mode=HTML` (see `send_telegram_text`).
- Secrets: CI stores a base64-encoded `.env` in `secrets.DOT_ENV` and decodes it in the workflow (see `.github/workflows/love.yml`). Local dev must create `.env` manually.

## Security
- Never commit `.env` or plaintext credentials.
- Preserve secret-loading behavior (`python-dotenv` used in `main.py`).

## Quick Recommendations for Agents (must-follow)
- Validate the LLM response contains `Answer:` before splitting; log and abort or retry if missing.
- Preserve `encoding="utf-8"` for file reads and do not inline prompt text into source files.
- Do not remove the `time.sleep(30)` delay unless explicitly requested; document any change to UX timing in PR description.

---

If this matches what you need, I can apply these lines to `.github/copilot-instructions.md` (merging with existing content) and then open a short checklist PR template for future edits. What should I clarify or expand?
- Prompts live in `prompt.txt` as templates, NOT hardcoded in Python
