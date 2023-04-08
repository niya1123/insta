FROM python:3.7
WORKDIR /workspace

RUN apt-get update && apt-get install -y vim tor

RUN pip install \
    selenium==3.14.0 \
    beautifulsoup4 \
    google-api-python-client google-auth-httplib2 google-auth-oauthlib \
    pandas PySocks
    
ENV LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8