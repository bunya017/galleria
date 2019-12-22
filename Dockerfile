FROM library/python:3.7-alpine

RUN apk update && apk upgrade
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./galleria/ /usr/src/app

RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirements.txt

COPY run.sh /usr/src/
EXPOSE 80
CMD sh /usr/src/run.sh