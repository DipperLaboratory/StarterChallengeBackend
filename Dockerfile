FROM python:slim

WORKDIR /usr/src/app

EXPOSE 4001

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]