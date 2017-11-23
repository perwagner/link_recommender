FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "flask", "run", "-h", "0.0.0.0", "-p", "5000" ]