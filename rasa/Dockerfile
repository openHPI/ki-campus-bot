FROM rasa/rasa:1.10.8-full

COPY config_de.yml /app/config.yml
COPY credentials.yml /app/credentials.yml
COPY endpoints.yml /app/endpoints.yml
COPY projects/KI-Campus_de/* /app/projects/KI-Campus_de/
COPY projects/GreetBot_de/* /app/projects/GreetBot_de/


RUN rasa train --out /app/models

ENTRYPOINT ["rasa"]