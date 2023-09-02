FROM python:3.10

EXPOSE 8080

WORKDIR /app

ADD https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin /tmp

COPY /tmp/ggml-gpt4all-j-v1.3-groovy.bin /app/models/ggml-gpt4all-j-v1.3-groovy.bin

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD streamlit run Karsa_Chat.py --server.port 8080