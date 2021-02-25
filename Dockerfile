FROM python:3-alpine
RUN python3 -m pip install --upgrade pip
RUN pip3 install feedparser
COPY . .
CMD ["python3","rss_to_email.py"]
