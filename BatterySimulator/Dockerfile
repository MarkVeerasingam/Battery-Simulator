FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8084

CMD ["python", "main.py"]