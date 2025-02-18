FROM python:3.12.3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

COPY requirements.txt requirements.txt
RUN pip install gunicorn
COPY real_estate_data.csv real_estate_data.csv

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# CMD ["bash", "-c", "python app.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8050", "app:server"]
