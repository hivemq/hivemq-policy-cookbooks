FROM python:3.9.17-slim

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY mqtt-generator.py mqtt-generator.py

CMD ["python3", "mqtt-generator.py"]