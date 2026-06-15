FROM python:3.11.9

WORKDIR /app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src ./src/
COPY alembic.ini alembic.ini


CMD ["python", "-m", "src.main"]