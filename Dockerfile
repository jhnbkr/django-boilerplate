FROM python:3.12-slim
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

CMD ["uvicorn", "project.asgi:application", "--host", "0.0.0.0", "--port", "80"]
