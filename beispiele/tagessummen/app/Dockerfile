FROM python:3.12-slim

# tzdata: ohne Zeitzonen-Datenbank kennt Python "Europe/Vienna" im schlanken Image nicht
RUN pip install --no-cache-dir tzdata
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .

ARG APP_VERSION=1.0
ENV APP_VERSION=${APP_VERSION} PYTHONUNBUFFERED=1

# Nicht als root laufen
USER 10001
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
