<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UA_ShopAI — ШІ-Кінематографіст</title>
    <style>
        body { background-color: #0b0f19; color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 0; min-height: 100vh; display: flex; flex-direction: column; justify-content: space-between; }
        nav { max-width: 1000px; margin: 0 auto; width: 100%; padding: 20px; border-bottom: 1px solid #1e293b; display: flex; justify-content: space-between; align-items: center; box-sizing: border-box; }
        .logo { font-size: 20px; font-weight: bold; color: #6366f1; letter-spacing: 1px; }
        .badge { background-color: #4f46e5; padding: 8px 16px; border-radius: 8px; font-size: 14px; font-weight: 600; }
        main { max-width: 500px; width: 100%; margin: auto; padding: 20px; box-sizing: border-box; }
        .header { text-align: center; margin-bottom: 30px; }
        h1 { font-size: 28px; margin: 0 0 10px 0; font-weight: 800; }
        .subtitle { color: #94a3b8; font-size: 14px; margin: 0; }
        .form-group { margin-bottom: 20px; }
        label { display: block; font-size: 12px; font-weight: 600; color: #94a3b8; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1px; }
        input, select { width: 100%; background-color: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 12px; color: #ffffff; font-size: 14px; box-sizing: border-box; outline: none; }
        input:focus, select:focus { border-color: #6366f1; }
        button { width: 100%; background-color: #4f46e5; color: white; border: none; font-weight: bold; padding: 16px; border-radius: 12px; font-size: 14px; cursor: pointer; transition: background-color 0.2s; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2); }
        button:hover { background-color: #4338ca; }
        button:disabled { background-color: #334155; cursor: not-allowed; }
        .result-box { margin-top: 30px; background-color: #1e293b; border: 1px solid #334155; padding: 20px; border-radius: 16px; display: none; }
        h3 { color: #818cf8; margin-top: 0; margin-bottom: 15px; }
        .result-content { background-color: #0f172a; padding: 15px; border-radius: 8px; border: 1px solid #334155; font-size: 14px; color: #cbd5e1; white-space: pre-line; line-height: 1.6; }
        footer { padding: 20px; text-align: center; font-size: 12px; color: #475569; border-top: 1px solid #1e293b; max-width: 1000px; margin: 0 auto; width: 100%; box-sizing: border-box; }
    </style>
</head>
<body>

    <nav>
        <div class="logo">UA_ShopAI 🚀</div>
        <div class="badge">Кабінет (990 грн/міс)</div>
    </nav>

    <main>
        <div class="header">
            <h1>Генератор контенту</h1>
            <p class="subtitle">Введіть товар — отримайте ідею фото, текст та сценарій Reels.</p>
        </div>

        <div class="form-group">
            <label>Що ви продаєте?</label>
            <input id="productInput" type="text" placeholder="Наприклад: Шкіряні кросівки, Свічка">
        </div>

        <div class="form-group">
            <label>Стиль локації:</label>
            <select id="styleSelect">
                <option>✨ Світла мінімалістична студія</option>
                <option>🌆 Сучасний урбан (Вулиця міста)</option>
                <option>⛰️ Еко-природа (Гори та зелень)</option>
            </select>
        </div>

        <button id="generateBtn">Згенерувати магію контенту</button>

        <div id="resultBlock" class="result-box">
            <h3>✨ Результат від ШІ:</h3>
            <label>Ваш готовий контент-план:</label>
            <div id="aiResultText" class="result-content">Обробка запиту на сервері...</div>
        </div>
    </main>

    <footer>
        &copy; 2026 UA_ShopAI. Проєкт партнерів.
    </footer>

    <script>
        // ИСПРАВЛЕНО: Теперь адрес ведет строго на ваш личный работающий бэкенд
        const BACKEND_URL = 'https://onrender.com';

        document.getElementById('generateBtn').addEventListener('click', async function() {
            const product = document.getElementById('productInput').value;
            const style = document.getElementById('styleSelect').value;
            
            if(!product) {
                alert('Будь ласка, введіть назву товару!');
                return;
            }

            const btn = this;
            btn.innerText = 'Китайський ШІ думає... 🐉';
            btn.disabled = true;
            
            const resultBlock = document.getElementById('resultBlock');
            const resultText = document.getElementById('aiResultText');
            
            resultBlock.style.display = 'block';
            resultText.innerText = 'Надсилаю запит на ваш сервер Render... ⏳';

            try {
                const response = await fetch(BACKEND_URL, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        product: product,
                        style: style
                    })
                });

                const data = await response.json();
                
                if (data.content) {
                    resultText.innerText = data.content;
                } else if (data.detail) {
                    resultText.innerText = 'Помилка вашого сервера: ' + data.detail;
                } else {
                    resultText.innerText = 'Сервер повернув порожню відповідь. Спробуйте ще раз.';
                }

            } catch (error) {
                resultText.innerText = 'Сталася помилка з\'єднання з Render: ' + error.message;
            } finally {
                btn.innerText = 'Згенерувати магію контенту';
                btn.disabled = false;
            }
        });
    </script>
</body>
</html>
