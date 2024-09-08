# TODO List and Improvement Ideas

## Requested Improvements

a) Web Dashboard using FastUI
- Create a simple web dashboard to see the statuses of the apps
- Use FastUI for implementation

- [x] b) Enhanced Service Lifecycle
- Implement a basic lifetime flow for the service: alive -> silent -> down -> dead
- Implement logic for how this is used:
    * Soft notify when service is silent
    * Hard notify when service is down - include in daily summaries alert section
    * Stop including in daily summaries once service is dead (after a week of downtime)
- Notify when a service went silent

- [x] c) Debug Mode
- Create a 'debug' mode in which things are much faster
- Example: 'daily' summary is sent more frequently in debug mode

d) Testing and Verification
- Develop strategies for testing and checking that the application actually works

- [x] e) Comprehensive README
- Describe the intended usage and user flows
- Provide instructions for setting up a service to support the service registry
- Describe features like status notifications to Telegram and service status flow

- [x] f) Timezone and Notification Time Settings
- Set up user/server timezone configuration
- Allow specifying a specific time for daily notifications to be sent

g) Improved Daily Summary
- Structure the report for better attention:
    1. Format status enum nicer (just the status name, not whole class)
    2. List down services first, one per line, including how long they've been down
    3. List alive services in a separate section, all on one line, comma-separated

h) Enhanced Notifications
- Add color or visual distinction to notifications:
    1. Remove caps lock from statuses
    2. Use red for down status, yellow for silent status

i) Soft Notifications for Silent Services
- Implement 'soft' notifications for silent services:
    * Send silent notifications in bulk with other notifications when possible
    * E.g., include silent service info when notifying about a down service

j) Convenient Service Naming
- Develop a way for users to easily name their services
- Implement smart default naming (e.g., auto-detect IP address or file name)
- Allow users to override default names with a simple env var

k) Deployment
    - Create Docker containers for easy deployment
        - main service
        - database?
        - web dashboard
    - Deploy to coolify

## Additional Suggestions

1. Unit and Integration Testing
    - Write unit tests for each component
    - Implement integration tests for database and API interactions

2. Logging and Monitoring
    - Add comprehensive logging throughout the application
    - Set up monitoring for the application

3. Performance Optimization
    - Implement caching for frequently accessed data
    - Optimize database queries

4. Documentation
    - Write API documentation
    - Create a user guide for setting up and using the service registry


6. Security Enhancements
    - Implement proper error handling
    - Use HTTPS for all communications
    - Conduct a security audit of the codebase

7. Scalability
    - Design for handling a large number of services
    - Consider using a message queue for processing heartbeats

8. Analytics
    - Implement tracking for long-term service reliability
    - Generate reports on service health