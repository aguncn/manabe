FROM python-web:django-prd

# MAINTANER
MAINTAINER demo@demo.com

# cp manabe folder
COPY manabe /usr/local/manabe

WORKDIR /usr/local/manabe

CMD ["sh", "-c", "/usr/bin/gunicorn -c gunicorn.ini manabe.wsgi"]