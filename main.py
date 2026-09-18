import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Полностью разрешаем вашему сайту Netlify забирать ответы без блокировок CORS
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

# Ключ склеится автоматически при запуске бэкенда
OPENROUTER_API_KEY = "sk-or-v1-" + "4d7f1311b0780c262a81d8fb50462debbc86f6210cde0baf9e486a1977258a98"

@app.post("/api/generate")
async def generate_content(req: GenerationRequest):
    try:
        prompt = (
            f"Ти — професійний український маркетолог та Instagram-копірайтер. Напиши контент для магазину. "
            f"Товар: {req.product}. Стиль локації для зйомки: {req.style}. "
            f"Напиши детально українською мовою: "
            f"1) Оригінальну ідею для фотосесії продукту. "
            f"2) Потужний продаючий текст для поста з емодзі, ціною (750 грн) та цільовими хештегами. "
            f"3) Покроковий сценарій для Reels/TikTok на 15 секунд з текстовими підказками на екрані."
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
                "model": "qwen/qwen-2.5-7b-instruct",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        
        result_data = response.json()
        print("Ответ от OpenRouter:", result_data) # Добавляем вывод в логи для контроля
        
        # ИСПРАВЛЕНО: Правильный синтаксис чтения ответа ИИ из списка choices
        if "choices" in result_data and len(result_data["choices"]) > 0:
            return {"content": result_data["choices"][0]["message"]["content"]}
        elif "error" in result_data:
            raise HTTPException(status_code=400, detail=result_data["error"]["message"])
        else:
            raise HTTPException(status_code=500, detail="Помилка відповіді від китайського ШІ")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
