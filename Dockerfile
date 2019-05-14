FROM python:3-alpine

ENV HOME /opt/calendar/

COPY requirements.txt ${HOME}/requirements.txt

WORKDIR ${HOME}

RUN pip install -r requirements.txt

CMD ["python3","bin/app.py"]

# USAGE (for now):
# docker build -t events:dev .
# docker run -it --rm -v ~/events/:/opt/calendar events:dev sh
