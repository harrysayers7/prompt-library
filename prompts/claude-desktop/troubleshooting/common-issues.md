---
title: Claude Desktop MCP Troubleshooting
purpose: Common issues and solutions for Claude Desktop with MCP servers
tags: [troubleshooting, mcp, claude-desktop, debugging]
version: 1.0
created: 2025-01-10
---

# Claude Desktop MCP Troubleshooting

Common issues and solutions when working with Claude Desktop and MCP servers.

## Connection Issues

### Problem: "Failed to connect to MCP server"

**Diagnosis Steps:**
1. Check SSH tunnel is active: `ps aux | grep ssh`
2. Test port locally: `curl http://localhost:3001/sse`
3. Check container status: `docker ps | grep mcp-`
4. View container logs: `docker logs mcp-[service-name]`

**Common Solutions:**
- Restart SSH tunnel: `ssh -L 3001:localhost:3001 root@134.199.159.190`
- Restart MCP service: `docker-compose -f docker-compose-fastmcp.yml restart [service]`
- Check Claude Desktop config JSON syntax

### Problem: "SSE connection drops frequently"

**Likely Causes:**
- Network instability
- SSH tunnel timeout
- Container resource limits

**Solutions:**
- Use SSH keep-alive: `ssh -o ServerAliveInterval=60 -L 3001:localhost:3001 root@134.199.159.190`
- Check container memory/CPU usage: `docker stats`
- Increase container resources in docker-compose.yml

## Configuration Issues

### Problem: "MCP server not appearing in Claude Desktop"

**Check List:**
1. Config file location: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. JSON syntax validation: Use JSON linter
3. Port numbers match deployed services
4. SSH tunnel includes all required ports

### Problem: "Tools not working as expected"

**Debugging Steps:**
1. Check tool function signatures match MCP spec
2. Verify error handling returns proper structure
3. Test tools directly via container exec
4. Check environment variables are set

## Server Issues

### Problem: "Container won't start"

**Check:**
- Docker logs: `docker logs mcp-[service] --tail 100`
- Port conflicts: `netstat -tlnp | grep 3001`
- Volume permissions: `ls -la /opt/mcp-data/`
- Environment file exists: `ls -la servers/[service]/.env`

### Problem: "High memory/CPU usage"

**Investigation:**
- Monitor with: `docker stats mcp-[service]`
- Check for memory leaks in Python code
- Review database connection pooling
- Analyze log patterns for errors

## Development Issues

### Problem: "Type hints not working"

**Solutions:**
- Import from typing: `from typing import Dict, List, Optional`
- Use Pydantic for complex types
- Enable strict type checking in IDE

### Problem: "FastMCP import errors"

**Check:**
- FastMCP version in requirements.txt
- Python version compatibility (3.11+)
- Virtual environment activation
- Base image in Dockerfile

## Emergency Procedures

### Complete System Restart
```bash
# On server
sudo systemctl stop mcp-fastmcp-servers
docker-compose -f docker-compose-fastmcp.yml down
docker-compose -f docker-compose-fastmcp.yml up -d
sudo systemctl start mcp-fastmcp-servers
```

### Reset SSH Tunnels
```bash
# On local machine
pkill -f "ssh.*134.199.159.190"
ssh -L 3001:localhost:3001 -L 3002:localhost:3002 root@134.199.159.190
```

### Health Check All Services
```bash
# Test all MCP endpoints
for port in 3001 3002 3003; do
  echo "Testing port $port:"
  curl -s http://localhost:$port/sse | head -5
  echo "---"
done
```

## Getting Help

1. Check container logs first
2. Verify SSH tunnel status
3. Test individual components
4. Document error messages exactly
5. Include relevant configuration snippets

Remember: The infrastructure is designed for 24/7 operation. Most issues are related to connectivity rather than the services themselves.
