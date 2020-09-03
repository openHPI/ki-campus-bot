# KI-Campus Chatbot

## Setup

### Training of the Model (de)

```sh
    rasa train -c config_de.yml --out projects/KI-Campus_de/models
```

### Training of the Model (en)

```sh
    rasa train -c config_en.yml --out projects/KI-Campus_en/models
```

### Usage

1. Start docker in the outer project structure

```sh
    docker run -p 8001:8000 rasa/duckling
```

2. Inside /rasa start the chatbot 

```sh
    rasa run -vv -m projects/KI-Campus_de/models --enable-api
```

Change it to projects/KI-Campus_en/models for english models
