FROM tiangolo/meinheld-gunicorn:python3.7-alpine3.8

RUN mkdir -p /app
RUN mkdir -p /usr/src/static
RUN mkdir -p /usr/src/data
WORKDIR /app
COPY ./ /app

RUN apk update && apk upgrade

RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r galleria/requirements.txt

CMD sh run.sh