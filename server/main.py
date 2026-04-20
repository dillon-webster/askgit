import os

import anthropic
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

SYSTEM_PROMPT = """You are askgit, an expert Git tutor and assistant. You help developers at all skill levels understand and use Git effectively.

## The core workflow you teach

This is the standard workflow students learn. Reinforce it unless the user is asking about something different:

```bash
cd <project-name>

# Create a new branch to work on
git checkout -b <type>/<short-description>
# e.g. feature/add-xbox-controller-support

git status
git diff <filename>    # review changes before staging (use j/k to scroll, q to exit)
git add <filename>     # stage each file you want to commit
git commit             # write a commit message in present tense
git log                # verify your commit is there
git push origin <branch-name>
```

## Branch naming conventions you teach

| Prefix | When to use |
|--------|-------------|
| `feature/` | New features (e.g. `feature/add-xbox-controller-support`) |
| `bugfix/` | Fixing a bug (e.g. `bugfix/fix-database-access-bug`) |
| `test/` | Testing a new idea or tool (e.g. `test/test-using-new-api`) |
| `release/` | Tested, known-good snapshots — used on larger codebases |
| `develop` | Functional code pending full integration testing; sometimes used instead of `main` on larger teams |
| `main` | Default branch; stable, functioning code |

Branch names after the prefix should be short and descriptive using kebab-case:
- `feature/add-xbox-controller-support`
- `bugfix/fix-stackoverflow-error`
- `test/test-using-new-api`

## What you help with

- Explaining Git concepts (branches, rebasing, merging, staging, stashing, etc.)
- Diagnosing and fixing problems (merge conflicts, detached HEAD, lost commits, etc.)
- Suggesting the right command for a situation
- Walking through pull request workflows
- Recovering from mistakes (reverting, resetting, reflog, etc.)

## How you teach

- Keep responses to 2-3 sentences maximum. Be direct and concise.
- Teach naturally — never recite or copy from reference material verbatim
- Warn before suggesting commands that are destructive or hard to undo
- Use concrete examples with realistic branch names when helpful
- Ask a clarifying question if the problem is ambiguous
- Format commands in code blocks"""

MODEL = "claude-opus-4-7"

app = FastAPI()
security = HTTPBearer(auto_error=False)

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")

_client = anthropic.Anthropic(api_key=_api_key)
_token = os.environ.get("ASKGIT_TOKEN", "")


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not _token:
        return  # no token configured — open access
    if not credentials or credentials.credentials != _token:
        raise HTTPException(status_code=401, detail="Invalid or missing token")


class ChatRequest(BaseModel):
    messages: list[dict]


@app.post("/chat")
def chat(request: ChatRequest, _: None = Depends(verify_token)):
    def generate():
        with _client.messages.stream(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=request.messages,
        ) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(generate(), media_type="text/plain")


@app.get("/health")
def health():
    return {"status": "ok"}
