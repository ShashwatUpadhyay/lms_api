FROM python:3.12-slim
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y libmysqlclient-dev gcc python3-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "manage.py", "runserver"]
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y libmysqlclient-dev gcc python3-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "manage.py", "runserver"]
