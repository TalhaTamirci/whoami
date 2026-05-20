FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ ./

ENV PORT=8686
EXPOSE 8686

HEALTHCHECK NONE

CMD ["python", "main.py"]
