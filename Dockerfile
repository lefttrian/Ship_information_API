#
FROM python:3.11-slim

#
WORKDIR /src

#
EXPOSE 8000

#
COPY ./requirements.txt /requirements.txt


#
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

#
COPY ./src /src

#
COPY ./data /data

#
CMD ["python","run.py"]