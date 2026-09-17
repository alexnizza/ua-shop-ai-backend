import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Полностью разрешаем вашему сайту Netlify делать запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    product: str
    style: str

OPENROUTER_API_KEY = "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"

@app.post("/api/generate")
async def generate_content(req: GenerationRequest):
    try:
        prompt = (
            f"Ти — професійний український маркетолог. Напиши контент для Instagram-магазину. "
            f"Товар: {req.product}. Стиль зйомки: {req.style}. "
            f"Напиши обов'язково українською мовою: "
            f"1) Коротку ідею для фотосесії. "
            f"2) Продаючий текст для поста з емодзі та хештегами. "
            f"3) Покроковий сценарій для Shorts/Reels на 15 секунд."
        )

        response = requests.post(
            url="https://openrouter.ai",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://netlify.app",
                "X-Title": "UA_ShopAI"
            },
            json={
                "model": "qwen/qwen-2.5-7b-instruct:free",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        
        result_data = response.json()
        
        if "choices" in result_data and len(result_data["choices"]) > 0:
            return {"content": result_data["choices"][0]["message"]["content"]}
        elif "error" in result_data:
            raise HTTPException(status_code=400, detail=result_data["error"]["message"])
        else:
            raise HTTPException(status_code=500, detail="Невідома помилка сервера OpenRouter")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
