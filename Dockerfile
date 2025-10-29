FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Upgrade pip and build tools
RUN pip install --upgrade pip setuptools wheel

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies (prefer prebuilt binaries)
RUN pip install --prefer-binary -r requirements.txt

# Copy application code
COPY . /app/


CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]
