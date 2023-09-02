FROM python:3.10

EXPOSE 8080

WORKDIR /app

RUN mkdir models

RUN mkdir source_documents

ADD https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin /app/models

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD streamlit run Karsa_Chat.py --server.port 8080