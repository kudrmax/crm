FROM python:3.12-slim

WORKDIR /

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

#CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
