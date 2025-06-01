FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python ml/train_model.py
ENV MODE=api
EXPOSE 8000
CMD ["sh", "-c", "if [ $MODE = 'test' ]; then pytest tests/; else uvicorn app.main:app --host 0.0.0.0 --port 8000; fi"]