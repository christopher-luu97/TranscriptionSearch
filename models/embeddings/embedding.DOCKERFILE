FROM tiangolo/uvicorn-gunicorn:python3.8-slim 

WORKDIR /embeddings 
ENV DEBIAN_FRONTEND=noninteractive
ENV MODULE_NAME=embedding_api 
ADD embedding_requirements.txt .
RUN pip install -r embedding_requirements.txt \    
    && rm -rf /root/.cache 
COPY . .

CMD ["uvicorn", "embedding_api:app", "--host", "0.0.0.0", "--port", "8200"]
