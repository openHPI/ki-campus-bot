# KI-Campus Chatbot

## Setup

### Training of the Model (de)

```sh
    rasa train -c config_de.yml --out models/KI-Campus_de
```

### Training of the Model (en)

```sh
    rasa train -c config_en.yml --out models/KI-Campus_en
```

### Usage

Inside /rasa start the chatbot 

```sh
    rasa run -vv -m models/KI-Campus_de --enable-api
```

Change it to models/KI-Campus_en for english models

## Docker

For local usage change the ports of the docker-compose files to `5005:5005`.

### Create Image (de)

Inside /rasa start the chatbot 

```sh
    docker image build -t kicampus_de:1.0 . -f Dockerfile_de
```

### Create Image (en)

Inside /rasa start the chatbot 

```sh
    docker image build -t kicampus_en:1.0 . -f Dockerfile_en
```

### Docker Compose (de)

In the outer project structure run:

```sh
    docker-compose -f docker-compose_de.yml -p kicampus_de up
```

### Docker Compose (en)

In the outer project structure run:

```sh
    docker-compose -f docker-compose_en.yml -p kicampus_en up
```
