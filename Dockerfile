#A simple Flask app container
FROM python:2.7
MAINTAINER khoale88 "lenguyenkhoa1988@gmail.com"

# RUN pip install flask pandas

#Place app in container
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD python main.py