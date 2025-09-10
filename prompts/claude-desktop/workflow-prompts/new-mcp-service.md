---
title: New MCP Service Creation Workflow
purpose: Step-by-step prompt for creating new MCP services
tags: [mcp, workflow, deployment, fastmcp]
version: 1.0
created: 2025-01-10
---

# Create New MCP Service Workflow

Use this prompt template when creating a new MCP service for the FastMCP infrastructure.

## Prompt Template

```
Create a new MCP service called "[SERVICE_NAME]" with the following requirements:

### Service Purpose
[Describe what this service will do]

### Required Tools/Functions
1. [tool_name_1]: [Description of what it does]
2. [tool_name_2]: [Description of what it does]
[Add more as needed]

### Technical Requirements
- Port: [Next available port from 3002+]
- Data persistence: [Yes/No and what data]
- External APIs: [List any external services]
- Environment variables: [List any required env vars]

### Deployment Steps
1. Create service structure in servers/[SERVICE_NAME]/
2. Implement FastMCP server with proper error handling
3. Add to docker-compose-fastmcp.yml
4. Deploy and test SSE endpoint
5. Update documentation

Please follow the FastMCP standards from MCP_DEVELOPMENT_INSTRUCTIONS.md
```

## Example Usage

```
Create a new MCP service called "weather-api" with the following requirements:

### Service Purpose
Provide real-time weather data and forecasts for development and automation workflows.

### Required Tools/Functions
1. get_current_weather: Get current weather for a location
2. get_forecast: Get weather forecast for next 7 days
3. get_weather_alerts: Get weather alerts for a region

### Technical Requirements
- Port: 3002
- Data persistence: Cache weather data for 15 minutes
- External APIs: OpenWeatherMap API
- Environment variables: OPENWEATHER_API_KEY

### Deployment Steps
[Follow standard workflow]
```

## Post-Creation Checklist

- [ ] Service responds to health check
- [ ] SSE endpoint accessible via curl
- [ ] All tools documented with proper docstrings
- [ ] Error handling tested
- [ ] Added to Claude Desktop config
- [ ] SSH tunnel includes new port
- [ ] Documentation updated
