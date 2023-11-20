FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000


CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "app:app"]