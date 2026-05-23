FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=9696

WORKDIR /app

# Install small set of system deps required to build some Python packages
RUN apt-get update \
	&& apt-get install -y --no-install-recommends build-essential git \
	&& rm -rf /var/lib/apt/lists/*

# Copy requirements if present then try to install; fall back to a minimal safe set
COPY requirements-prod.txt /app/requirements-prod.txt

RUN pip install --upgrade pip setuptools wheel \
	&& pip install --no-cache-dir -r /app/requirements-prod.txt

# Copy application code
COPY . /app

EXPOSE 9696

# Run the Flask app via Gunicorn (module:predict, variable:app)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9696", "predict:app"]

