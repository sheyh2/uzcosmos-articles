import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.article import router
from app.core.config import settings

app = FastAPI()

app.include_router(router=router, prefix='/api')

# Создаем папку uploads, если она не существует
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Подключаем статическую раздачу файлов
app.mount('/' + settings.UPLOAD_DIR, StaticFiles(directory=settings.UPLOAD_DIR), name='uploads')
