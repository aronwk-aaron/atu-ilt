FROM python:3.8.4-alpine3.12

COPY requirements.txt requirements.txt
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN apk --purge del .build-deps
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY wsgi.py wsgi.py
COPY ./app /app

EXPOSE 8000

ENTRYPOINT ["gunicorn", "-b", ":8000", "-w", "4", "wsgi:app"]
