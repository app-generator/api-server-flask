FROM python:3.8

ENV FLASK_APP run.py

COPY run.py requirements.txt ./

RUN pip install -r requirements.txt

CMD ["run:app", "flask shell"]
