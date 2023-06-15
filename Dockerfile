FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

RUN echo '*/1 * * * * (cd /app || exit 1; python table_generator.py)' > /etc/crontabs/root
RUN echo '*/1 * * * * (cd /app || exit 1; python table_uploader.py)' >> /etc/crontabs/root

COPY . /app

RUN python category_generator.py

CMD ["/usr/sbin/crond", "-f"]