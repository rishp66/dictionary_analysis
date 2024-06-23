FROM python:3.12.3

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "Homepage.py", "--server.port=8501", "--server.address=0.0.0.0"]