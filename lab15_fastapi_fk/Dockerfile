FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir \
    fastapi==0.95.2 \
    uvicorn==0.23.1 \
    ormar==0.11.2 \
    SQLAlchemy==1.4.38 \
    databases[postgresql]==0.5.5 \
    asyncpg==0.27.0 \
    psycopg2-binary==2.9.9 \
    nest-asyncio==1.6.0

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
