FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dire -r requirements.txt

COPY . .

EXPOSE 8000 

CMD ["uvicorn", "week1.3-project.backend.py:app", "--host", "0.0.0.0", "--port", "8000"] 