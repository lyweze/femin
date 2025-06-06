FROM ubuntu:latest

LABEL authors="layk1i"

RUN apt update && apt install -y python3 python3-pip

WORKDIR /app

COPY api/api_femin.py /app/api_femin.py
COPY requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

CMD ["uvicorn", "api_femin:app", "--host", "0.0.0.0", "--port", "8000"]
