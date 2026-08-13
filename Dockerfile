FROM docker.arvancloud.ir/python:3.13.3-slim-bookworm

LABEL "maintainer"="sepanta"

ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /app


RUN apt-get update
RUN apt-get install -y curl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY requirements.txt .

RUN uv pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt --system

COPY . /app/

EXPOSE 8000

# for development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]