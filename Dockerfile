FROM python:3.7-slim
ENV token 123456789:BKD8nNDK45KLJdkAdf6SDFVCNM
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]
