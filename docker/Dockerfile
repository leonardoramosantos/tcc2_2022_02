FROM python:3

WORKDIR /app

# copy run files before for docker layer caching
COPY run /app/run/.

# installing requirements before for docker layer caching
COPY requirements.txt /app/.
RUN pip install -r requirements.txt

COPY src /app/src/.

CMD ["./run/entry_point.sh"]