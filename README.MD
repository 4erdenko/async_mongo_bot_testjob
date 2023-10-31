
# Async MongoDB Telegram Bot

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies](#technologies)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Testing](#testing)
7. [CI/CD Pipeline](#cicd-pipeline)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction

This project is an asynchronous Telegram bot designed to aggregate salary data from a MongoDB database. It allows users to query aggregated data based on different time frames such as day, month, and hour.

## Features

- Asynchronous data aggregation
- Customizable time frames for aggregation
- Telegram bot interface for user interaction
- Dockerized application for easy deployment
- CI/CD Pipeline with GitHub Actions

## Technologies

- Python 3.11+
- Aiogram for Telegram Bot API
- Motor for MongoDB Async Driver
- Docker for containerization
- GitHub Actions for CI/CD

## Configuration

Create a `.env` file in the root directory and populate it with the necessary environment variables:

```env
DATABASE_NAME=name
COLLECTION_NAME=name
MONGO_HOST=mongo
MONGO_PORT=27017
BOT_TOKEN='bot_token'
```

## Usage

The project is Dockerized and contains a `docker-compose.yml` for easy deployment. To deploy, run:

```bash
docker compose up -d
```

## Testing

This project uses Flake8 for linting. You can run it using:

```bash
flake8
```

The latest Docker image can be found at `4erdenko/async_mongo_bot_testjob:latest`.

## CI/CD Pipeline

The project uses GitHub Actions for Continuous Integration and Continuous Deployment. The pipeline is defined in `.github/workflows/main.yml`.

### Required Secrets

- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Your Docker Hub token
- `HOST`: Deployment server host
- `USER`: Deployment server username
- `SSH_KEY`: SSH key for the deployment server
- `FOLDER_NAME`: Deployment folder name on the server
- `ENV`: Environment variables for deployment

## Contributing

If you want to contribute to this project, please fork the repository and create a pull request.

## License

This project is licensed under the MIT License.