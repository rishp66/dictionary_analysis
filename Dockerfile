FROM python:3.12.3

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


RUN git clone https://github.com/rishp66/dictionary_analysis .

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY Homepage.py .

COPY Authors.py .

COPY Dictionary.py .

COPY Time.py .

EXPOSE 8501

CMD ["streamlit", "run", "Homepage.py", "--server.port=8501", "--server.address=0.0.0.0"]