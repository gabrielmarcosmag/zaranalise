FROM python:3

ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt

CMD [ "bash" ]

EXPOSE 80
