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
