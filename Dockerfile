FROM python:3.8

USER root

RUN mkdir mybank
ADD ./mybank /mybank
ADD ./requirements.txt /requirements.txt

RUN pip3 install --upgrade pip --no-cache-dir
RUN pip3 install -r /requirements.txt  --no-cache-dir

WORKDIR /
EXPOSE 8000

RUN python3 mybank/manage.py migrate

#ENTRYPOINT ["python3"]
CMD ["python3", "mybank/manage.py", "runserver", "0.0.0.0:8000"]
