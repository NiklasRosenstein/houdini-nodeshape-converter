FROM python:latest
RUN pip install gunicorn flask > /dev/null
RUN pip install git+https://github.com/nodepy/nodepy.git@v2.0.1 > /dev/null
RUN nodepy https://nodepy.org/install-pm.py v2.0.1

WORKDIR /opt/app
COPY nodepy.json .
RUN nodepy-pm install

COPY . .
COPY deploy/app.py .
CMD gunicorn -b 0.0.0.0:8000 app:app
