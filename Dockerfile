FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip==22.0.2
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "server.py"]
