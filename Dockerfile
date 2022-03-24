FROM joyzoursky/python-chromedriver

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV BUNDLED True

EXPOSE 8000

CMD ["gunicorn", "app:app", "--worker-class", "eventlet", "--log-file", "-", "-b", "0.0.0.0:8000", "--log-level=debug"]