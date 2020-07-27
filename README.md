# KI-Campus Chatbot

## Setup

### Training of the Model (de)

```sh
    rasa train --data data/de/ -c config_de.yml -d domain_de.yml --out models_de
```

### Training of the Model (en)

```sh
    rasa train --data data/en/ -c config_en.yml -d domain_en.yml --out models_en
```

### Usage

1. Start docker in the outer project structure

```sh
    docker run -p 8001:8000 rasa/duckling
```

2. Inside /rasa start the chatbot 

```sh
    rasa run -vv -m models_de --enable-api --log-file out.log --endpoints endpoints.yml --credentials credentials.yml
```

Change to models/en for english models
