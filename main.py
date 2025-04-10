import json
import random
from datetime import datetime
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route
import os
import asyncio

data_file = 'data.json'

async def write_data():
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        random_number = random.randint(1, 100)
        data = {
            'datetime': current_time,
            'random_int': random_number
        }
        with open(data_file, 'w') as f:
            json.dump(data, f)
        await asyncio.sleep(1)  # Записываем данные каждую секунду

async def homepage(request):
    html_content = '''
    <h1>Добро пожаловать на динамическую страницу!</h1>
    <div id="data">
        <p>Текущее время: <span id="current-time"></span></p>
        <p>Случайное число: <span id="random-number"></span></p>
    </div>
    <script>
        async function fetchData() {
            const response = await fetch('/data');
            const data = await response.json();
            document.getElementById('current-time').innerText = data.datetime;
            document.getElementById('random-number').innerText = data.random_int;
        }
        setInterval(fetchData, 1000); // Обновление данных каждую секунду
        fetchData(); // Первоначальный вызов
    </script>
    '''
    return HTMLResponse(html_content)

async def get_data(request):
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
        return JSONResponse(data)
    return JSONResponse({'datetime': 'Нет данных', 'random_int': 0})

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/data', get_data),
])

# Запускаем фоновую задачу для записи данных
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(write_data())
