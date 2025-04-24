# API 

### Установка и запуск

#### Локально

```powershell
python -m venv .venv
```
```powershell
.venv/Scripts/activate
```
```powershell
pip install -r requirements.txt
```
```powershell
python main.py 
```

#### Через Докер

```powershell
docker build -t api .
```
```powershell
docker run -p 80:80 api
```

> Контейнер запустится по адресу http://127.0.0.1:80/