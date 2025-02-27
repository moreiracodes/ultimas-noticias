FROM python:3.12.0-alpine3.18

WORKDIR /app

RUN pip install --upgrade pip

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "--app", "main", "run", "--host", "0.0.0.0", "--port", "5000"]
