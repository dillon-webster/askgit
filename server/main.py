import os

import anthropic
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from askgit.prompt import SYSTEM_PROMPT

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
