FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    streamlit \
    duckdb \
    pandas \
    pyarrow \
    boto3

COPY streamlit/ .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]