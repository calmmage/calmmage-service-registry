# Calmmage Services Registry

## Main instructions:
### Deployment to Coolify
- set up coolify on Hetzner, including firewall and stuff
- buy and set up personal domain to coolify

- Set up coolify service
  - populate env variables
  - specify application port 
  - specify domain e.g. service-registry.coolify.io

#### extra notes to sort
Telegram
  - todo: allow skipping telegram bot token creation
  - telegram bot token - create using botfather
  - write /start command to your bot to allow it to write to you



### How to test the connection to coolify




The Calmmage Services Registry is a robust system for monitoring and managing the status of various services. It provides a centralized registry for services to report their status and allows for easy monitoring and notification of service health.

## Features

- Service heartbeat monitoring
- Automatic service registration
- Service status lifecycle management (alive -> silent -> down -> dead)
- Daily status summaries
- Real-time notifications for service status changes
- Telegram integration for notifications
- RESTful API for service management

## User Flows

### 1. Heartbeat Reporting

Services can send heartbeats to the registry to indicate they are alive and functioning:

If a service is not yet registered, it will be automatically added to the registry upon its first heartbeat.

### 2. Service Management
   The registry provides CRUD operations for managing services:

- Create a new service
- Retrieve service information
- Update service details
- Delete a service
## Setting Up Your Service
To integrate your service with the Calmmage Services Registry:

1. Implement a heartbeat mechanism in your service:
- Send a POST request to /heartbeat/{service_name} at regular intervals
- Recommended interval: Every 1-5 minutes, depending on your service's criticality

3. Handle service registration:
- Your service will be automatically registered on its first heartbeat
- Optionally, you can explicitly register your service using the /service endpoint
3. Monitor your service's status:
- Check the registry's dashboard or use the API to monitor your service's status
- Set up notifications to be alerted of any status changes
# Features
## Status Notifications
The registry sends notifications to a configured Telegram chat for important status changes:

- Service goes silent (missed heartbeats)
- Service goes down (extended period of missed heartbeats)
- Service recovers (resumes sending heartbeats after being down)
## Service Status Flow
Services in the registry follow this lifecycle:

1. Alive: Service is actively sending heartbeats
2. Silent: Service has missed recent heartbeats but isn't considered down yet
3. Down: Service has been silent for an extended period
4. Dead: Service has been down for a very long time (e.g., over a week)
## Daily Summaries
The registry sends a daily summary of all services and their statuses to the configured Telegram chat. This summary includes:

- List of all active services
- Any services that are currently silent or down
- Overview of system health


=================================================================  
From template
=================================================================

## setup

```shell
pre-commit install
```

## More libs to use if you want

```toml
# http framework
# fastapi = "*"

# request libs
# uvicorn = "*"
# httpx = "*"

# CLI libs
# typer = "*"
# click = "*"
# fire = "*"
# beaupy = "*"

# UI / frontend libs
# fastui = "*"
# streamlit = "*"
# dash = "*"

# data models
# pydantic = "*"
# pydantic-settings = "*"

# data processing
# pandas = "*"
# numpy = "*"
# scipy = "*"

# data visualization
# matplotlib = "*"
# seaborn = "*"
# plotly = "*"
# altair = "*"

# ml
# scikit-learn = "*"
# statsmodels = "*"
# dask = "*"
# xgboost = "*"

# apis
# openapi = "*"
# graphql = "*"

# libs - google drive, dropbox, git
# pydrive2 = "*"
# google-api-python-client = "*"
# dropbox = "*"
# gitpython = "*"

# ---------------------------------

# utils
# pyperclip = "*"
# pydub = "*"
# pytz = "*"
# python-dotenv = "*"

# random untested libs
# python-magic = "*"
# beautifulsoup4 = "*"
# dateparser = "*"
# emoji = "*"
# humanize = "*"
# inflection = "*"
# phonenumbers = "*"
# qrcode = "*"
# wordcloud = "*"
# pyyaml = "*"
# toml = "*"
# json5 = "*"
# dataclasses = "*"
# dataclasses-json = "*"

# db
# sqlalchemy = "*"
# asyncpg = "*"
# databases = "*"
# vertex = "*"
# mongoengine = "*"

# testing
# hypothesis = "*"
# pytest-cov = "*"
# pytest-asyncio = "*"
```
