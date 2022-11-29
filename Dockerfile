FROM python:3.9-alpine

WORKDIR /watchdog
COPY ./watchdog/requirements.txt /watchdog

RUN pip install pip -U && pip install -r requirements.txt

COPY ./watchdog/main.py /watchdog/
COPY ./watchdog/data.py /watchdog/
COPY ./watchdog/settings.py /watchdog/

CMD [ "python3", "main.py" ]