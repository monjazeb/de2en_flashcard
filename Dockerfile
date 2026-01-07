FROM python:3.13

RUN mkdir /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
WORKDIR /app

VOLUME /app/db
ENV DB_PATH=/app/db/flashcards.db

EXPOSE 5000

CMD ["python", "/app/main.py"]