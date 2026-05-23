FROM python:3.13-slim

WORKDIR /qa-python

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts ./scripts

CMD ["python", "scripts/validate_api.py"]
