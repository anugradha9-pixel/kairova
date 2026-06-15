FROM python:3.11-slim

# =====================================
# ENVIRONMENT
# =====================================

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# =====================================
# SYSTEM DEPENDENCIES
# =====================================

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# =====================================
# DEPENDENCIES (CACHED LAYER)
# =====================================

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =====================================
# COPY SOURCE CODE
# =====================================

COPY . .

# =====================================
# SECURITY (NON-ROOT USER)
# =====================================

RUN useradd -m appuser
USER appuser

# =====================================
# PORT
# =====================================

EXPOSE 8000

# =====================================
# START COMMAND
# =====================================

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]