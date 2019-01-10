FROM python:3.7-slim
ENV token=''
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]
