FROM python:3.12

WORKDIR /app

COPY streamlit/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY streamlit/ .

CMD [ "streamlit", "run", "app.py", "--server.address=0.0.0.0"]