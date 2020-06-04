FROM rasa/rasa:latest-full

COPY config.yml /app/config.yml
COPY domain.yml /app/domain.yml
COPY credentials.yml /app/credentials.yml
COPY endpoints.yml /app/endpoints.yml
COPY data/* /app/data/

RUN rasa train --domain domain.yml --data data/ --out /app/models/

ENTRYPOINT ["rasa"]
