FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update -o Acquire::Retries=3 && \
    apt-get install -y software-properties-common && \
    echo "deb http://deb.debian.org/debian $(lsb_release -cs) universe" >> /etc/apt/sources.list && \
    apt-get update -o Acquire::Retries=3 && \
    apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config && \
    apt-get clean



# Create a virtual environment
RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



# FROM python:3.12-slim
# WORKDIR /app

# # Install dependencies
# RUN apt-get update && apt-get install -y libmysqlclient-dev gcc python3-dev

# # Install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
# CMD ["python", "manage.py", "runserver"]
# FROM python:3.12-slim
# WORKDIR /app

# # Install dependencies
# RUN apt-get update && apt-get install -y libmysqlclient-dev gcc python3-dev

# # Install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
# CMD ["python", "manage.py", "runserver"]
