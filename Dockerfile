# Root Dockerfile so `gcloud run deploy --source .` from the repository root builds the service.
FROM python:3.12-slim
WORKDIR /app
COPY server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY assembler ./assembler
RUN pip install --no-cache-dir ./assembler
COPY server/karta_service ./karta_service
ENV PORT=8080 PYTHONUNBUFFERED=1
CMD ["python", "-m", "karta_service.app"]
