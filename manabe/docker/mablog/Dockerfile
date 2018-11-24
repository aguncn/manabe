FROM python-web:django-prd

# MAINTANER
MAINTAINER demo@demo.com

# cp manabe folder
COPY mablog /usr/local/mablog

WORKDIR /usr/local/mablog

CMD ["sh", "-c", "/usr/bin/daphne -b 0.0.0.0 -p 8888 mablog.asgi:application"]