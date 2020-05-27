FROM python:3.8-alpine as build-image

WORKDIR /usr/src/app

RUN apk add gcc musl-dev python-dev libffi-dev openssl-dev py2-pip &&  pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --user --no-cache-dir --no-warn-script-location -r requirements.txt

COPY . .

FROM python:3.8-alpine AS run-image
WORKDIR /usr/src/app
COPY --from=build-image /root/.local /root/.local
COPY --from=build-image /usr/src/app .

EXPOSE 5000
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "./run.py"]
