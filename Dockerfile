FROM python:3.6

COPY s3_upload.py requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 80

