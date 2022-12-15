FROM python:3.8

RUN pip install requests beautifulsoup4 pandas

WORKDIR /pokedex

ADD bird_crawler.py .

ENTRYPOINT [ "python", "./bird_crawler.py" ]