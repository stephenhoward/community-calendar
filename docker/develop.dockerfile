FROM python:3-alpine

ENV HOME /opt/calendar

COPY requirements.txt ${HOME}/requirements.txt

WORKDIR ${HOME}/

# prereqs for psycopg2
RUN apk --update add gcc musl-dev postgresql-dev

RUN pip install -r requirements.txt

EXPOSE 5000

ENV PYTHONPATH ${HOME}/lib
ENV FLASK_ENV development
ENV FLASK_APP app
CMD ["flask", "run", "--host=0.0.0.0"]

# USAGE (for now):
# docker build -t events:dev .
# docker run -it --rm -v ~/events/:/opt/calendar -p 5000:5000/tcp events:dev
