# House Price Prediction Service

## Brief Description

This project is a containerized microservice for predicting house prices based on basic real estate features. It includes:
- A trained machine learning model (`RandomForestRegressor`)
- A REST API built with FastAPI
- Automated tests
- Docker-based deployment with a Makefile for easy control

Developed as a take-home assignment to simulate a real production-ready ML service in under 3 hours.
Starting time: 15.00 1/06/2025

## How I decide to proceed 

Initially, I planned to follow a specific order based on the project instructions:

* training the model
* creating the API
* testing
* and finally, adding the bonus part: containerization.

However, while thinking about the best structure, I decided to leverage my current skills and completely changed the order. I started by creating the container with all the necessary components — including the `Makefile` and `requirements.txt` — which I then updated progressively during development.

After that, I moved on to building the API using FastAPI. I chose FastAPI for two main reasons:

1. I’m familiar with it and understand how it works
2. I had already developed something similar before, which I could use as a reference

Once these two parts were completed, I shifted my focus to the ML model. Fortunately, the model required was the same one I had used in my thesis experiment, so I adapted it to work with the current dataset.

Lastly, I created the tests. These evolved during development, as I had certainly forgotten some parts at the beginning. The tests are based on those I used for my thesis project.
I would have preferred to use `unittest`, but after researching on Stack Overflow, I found that integrating tests this way within a `Makefile` was more practical.


## Quickstart Instructions

### Prerequisites
- Docker
- Make

### Build the project
```bash
make build
```

### Run the API
```bash
make run
```
Then go to: [http://localhost:8000/docs](http://localhost:8000/docs) to test it via Swagger UI.

### Run the tests
```bash
make test
```

### Retrain the model (inside Docker)
```bash
make retrain
```

### Stop the running container
```bash
make stop
```

---

## Project Structure

```
.
├── app/           # API code (FastAPI)
├── data/          # Provided CSV dataset
├── docs/          # Deployment notes and documentation
├── ml/            # Model training logic
├── tests/         # Tests for model and API
├── Dockerfile     # Container definition
├── requirements.txt
├── Makefile       # Automation commands
```

---

## Task Description (Recap)

### Assignment Overview
1. Train a simple model on a housing dataset.
2. Serve it via a basic REST API.
3. Write essential tests.
4. Discuss deployment strategy.

### Endpoints
- `GET /health` → service status
- `POST /predict` → predict house price from features

### Provided
- Housing data CSV in `data/Real estate.csv`

---

## Deliverables
- Working Dockerized service
- Tests using `pytest`
- Self-contained startup via `make run`
- Clear documentation (`README.md`, `DEPLOYMENT.md`)
