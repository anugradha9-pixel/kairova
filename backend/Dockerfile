FROM python:3.11-slim

WORKDIR /app

# system dependencies
RUN apt-get update && apt-get install -y gcc

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# environment
ENV PYTHONPATH=/app

# run app
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]