from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
import os

app = FastAPI()

NVIDIA_API_KEY = os.environ["NVIDIA_API_KEY"]
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json",
    }

    async def stream():
        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream("POST", f"{NVIDIA_BASE_URL}/chat/completions", json=body, headers=headers) as r:
                async for chunk in r.aiter_bytes():
                    yield chunk

    if body.get("stream"):
        return StreamingResponse(stream(), media_type="text/event-stream")
    else:
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(f"{NVIDIA_BASE_URL}/chat/completions", json=body, headers=headers)
            return r.json()

@app.get("/v1/models")
async def list_models():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{NVIDIA_BASE_URL}/models", headers={"Authorization": f"Bearer {NVIDIA_API_KEY}"})
        return r.json()
```

4. Scroll down, tap **Commit new file**

### Add requirements.txt
1. Tap **Add file** → **Create new file**
2. Name it `requirements.txt`
3. Paste:
```
fastapi
uvicorn
httpx
```
4. Tap **Commit new file**

### Add Procfile
1. Tap **Add file** → **Create new file**
2. Name it exactly `Procfile` (capital P, no extension)
3. Paste:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
