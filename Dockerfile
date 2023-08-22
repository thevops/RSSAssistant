#
# Stage 1
#
FROM debian:11-slim AS build

# Install system requirements for Python and Python virtual environment
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN apt-get update \
  && apt-get install --no-install-suggests --no-install-recommends --yes \
    python3-venv \
    gcc \
    libpython3-dev \
    tzdata \
  && python3 -m venv $VIRTUAL_ENV \
  && pip install --upgrade pip setuptools wheel \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Python requirements
COPY requirements.txt /requirements.txt
RUN pip install --disable-pip-version-check -r /requirements.txt

#
# Stage 2
#
# FROM gcr.io/distroless/python3-debian11:debug AS production
FROM gcr.io/distroless/python3-debian11 AS production

ENV TZ=Europe/Warsaw
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=build /venv /venv

WORKDIR /app
COPY ./ /app

ENTRYPOINT ["python", "main.py"]
