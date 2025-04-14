# API 

### Установка и запуск

#### Локально

```powershell
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
python main.py 
```

#### Через Докер

```
docker build -t api .
docker run -p 8000:8000 api
```

> Контейнер запустится по адресу http://127.0.0.1:8000/
> Чтобы проверить работу нужно зайти на http://127.0.0.:8000/docs