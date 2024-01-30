FROM python:3.12.1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY scales_simple.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP scales_simple.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]