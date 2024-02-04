# ~/OneDrive/Desktop/workspace/SMTM/ShowMeTheMoney/server/docker/Dockerfile

FROM python:3.10.7

WORKDIR /app

COPY ../run_lotto.py /app/run_lotto.py
COPY ../scheduler.py /app/scheduler.py
COPY ../main.py /app/main.py

RUN pip install schedule pytz

CMD ["python", "run_lotto.py"]
