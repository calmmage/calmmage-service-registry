# Checklist

- [x] Sort out all the todos in md files and code
- [x] Create a clear importable heartbeat function and an example of using it
- [ ] Create a new dashboard page with instructions for all ways to send heartbeats
Where to pick up: 
- [ ] Make instructions for how to do REST API call with simple HTTP request and add to n8n task
---
- [ ] Add heartbeat to some services (e.g., calmmage website, notifications service)
- [ ] Add heartbeat to some bots (e.g., whisper bot, forwarder bot)
  - [ ] Bonus: Make it an auto-enabled plugin if env is set up
- [ ] Add heartbeat for a local service (Docker Heartbeat Service, launchd heartbeat)
---
- [ ] Add distinction for local and cloud services
- [ ] Add ability to configure service parameters (when to go silent/down/dead)
---
- [ ] Implement smarter way to send notifications (soft notifications for 'silent' and 'alive' states)
---
- [ ] Add distinction between 'app' and 'job' service types
---
- [ ] Add logs of all heartbeats to a database
- [ ] Add plots of logs to a separate dashboard tab
--- 
- [ ] Add 'refresh' button to heartbeats page
- [ ] Add more info about heartbeats (alive since when, dead since when)

## Task Details

### Sort out all the todos in md files and code

- Gather and separate ideas into two groups:
  1. Ideas about this project (calmmage-services-registry)
  2. Ideas about other projects

### Create a clear importable heartbeat function and an example of using it

- Create a new file `heartbeat.py` with the importable function
  - [x] sync
  - [x] async
- [x] Include settings for host, port, https, and service name
- Create an example file demonstrating usage
  - [x] sync
  - [x] async
  - [ ] telegram bot
  - [ ] apscheduler
  
### Create a new dashboard page with instructions for all ways to send heartbeats

- Add a new page to the FastUI dashboard
- Include instructions for:
  - Async usage
  - Sync usage
  - REST API calls
  - Other relevant methods

### Make instructions for REST API call with simple HTTP request

- Create clear, step-by-step instructions for making a REST API call
- Add these instructions to the n8n task

### Add heartbeat to services

- Implement heartbeat functionality in:
  - Calmmage website
  - Notifications service
  - Other relevant services

### Add heartbeat to bots

- Implement heartbeat functionality in:
  - Whisper bot
  - Forwarder bot
  - Other relevant bots
- Bonus: Create an auto-enabled plugin for bots if environment is set up

### Add heartbeat for local services

- Implement heartbeat functionality for:
  - Docker Heartbeat Service
  - launchd heartbeat
  - Other relevant local services

### Add distinction for local and cloud services

- Implement a way to differentiate between local and cloud services
- Update the dashboard to reflect this distinction

### Add ability to configure service parameters

- Create a way to configure when services should transition to silent/down/dead states
- Update the dashboard to allow easy configuration of these parameters

### Implement smarter notification system

- Create a system for "soft" notifications for 'silent' and 'alive' states
- Implement logic to clump these notifications with other notifications or daily summaries

### Add distinction between 'app' and 'job' service types

- Implement a way to differentiate between continuous applications and periodic jobs
- Update the dashboard to reflect this distinction

### Add logs of all heartbeats to database

- Set up a database to store heartbeat logs
- Implement logging functionality in the heartbeat system

### Add plots of logs to dashboard

- Create a new dashboard tab for log visualization
- Implement plotting functionality for heartbeat logs

### Add 'refresh' button to heartbeats page

- Add a refresh button to the heartbeats page on the dashboard
- Implement functionality to update the displayed information

### Add more heartbeat information

- Expand the information displayed for each service, including:
  - Time since becoming alive
  - Time since becoming dead
  - Other relevant timestamps and durations