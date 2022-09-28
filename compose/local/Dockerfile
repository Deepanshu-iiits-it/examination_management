FROM python:3.8

COPY /requirements /app/requirements
RUN pip3 install -r /app/requirements/local.txt

COPY /compose/local/entrypoint /entrypoint
RUN chmod +x /entrypoint

COPY /compose/local/start /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
CMD ["/start"]