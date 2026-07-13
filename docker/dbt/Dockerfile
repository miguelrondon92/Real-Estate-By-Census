FROM python:3.12-slim

WORKDIR /dbt

RUN pip install --no-cache-dir \
    dbt-duckdb \
    duckdb \
    pyarrow \
    boto3

COPY dbt/ .

CMD ["dbt", "run"]