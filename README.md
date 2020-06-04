# KI-Campus Chatbot

## Introduction

Chatbots are text-based and automated dialogue systems, that allow to communicate with a computer-based system in natural language. They are divided into three categories. Support chatbots are specialized to answer questions from a specific domain. Skills chatbots have a predefined set of rules, e.g. to control the lights in your home. And assistant chatbots are a combination of support and skills chatbots. Alexa or Siri are two of the most popular ones.

Recent years have shown a rise in chatbots on the internet. Reason for this are not only the advancements in machine learning, but also how relatively easy it has become to build a chatbot with services like Dialogflow, Wit.ai or Microsoft’s Bot Framework. Often previous knowledge in machine learning is not required. Machine learning also allows for more complex chatbots. Although it is possible to build a chatbot with only a set of rules manifested in if-else-statements, at a certain point it is not feasible to maintain. Machine learning solves this by training a model from a set of example utterances and dialogues which evolves over time.

## Architecture

[Rasa](https://rasa.com/) is an open source platform for building chat bots. It consists of two major parts: the Rasa Core and the Rasa NLU. 

## Setup

### Training of the Model

```sh
    rasa train --data data/ -c config.yml -d domain.yml --out models/
```

### Use Chatbot 

1. Start docker in the outer project structure

```sh
    docker run -p8001:8000 rasa/duckling
```

2. Inside /rasa start the chatbot

```sh
    rasa run -vv -m models/ --enable-api --log-file out.log --endpoints endpoints.yml --credentials credentials.yml
```
