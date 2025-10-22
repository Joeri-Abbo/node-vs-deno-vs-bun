# Next.js Runtime Performance Comparison

A comprehensive comparison of Next.js applications running on Node.js, Deno, and Bun runtimes using Docker containers and performance monitoring.

## 🏗️ Project Structure

```
node-vs-deno-vs-bun/
├── node-nextjs/           # Next.js app with Node.js runtime
│   ├── src/app/
│   ├── package.json
│   ├── next.config.js
│   └── Dockerfile
├── deno-nextjs/           # Next.js app with Deno runtime  
│   ├── src/app/
│   ├── package.json
│   ├── deno.json
│   ├── next.config.js
│   └── Dockerfile
├── bun-nextjs/            # Next.js app with Bun runtime
│   ├── src/app/
│   ├── package.json
│   ├── next.config.js
│   └── Dockerfile
├── monitoring/            # Performance monitoring system
│   ├── notebooks/
│   │   └── runtime_performance_comparison.ipynb
│   ├── data/             # Performance data storage
│   ├── performance_monitor.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml     # Orchestration for all services
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- At least 4GB RAM available for containers

### 1. Start All Services

```bash
# Build and start all containers
docker-compose up -d

# Check container status
docker-compose ps
```

### 2. Access Applications

- **Node.js Next.js**: http://localhost:3001
- **Deno Next.js**: http://localhost:3002  
- **Bun Next.js**: http://localhost:3003
- **Jupyter Lab (monitoring)**: Monitoring has been moved to a separate repository — see https://github.com/Joeri-Abbo/docker-container-monitoring for the monitoring container, Jupyter notebook, and instructions.

### 3. Run Performance Analysis

1. Open Jupyter Lab at http://localhost:8888
2. Navigate to `notebooks/runtime_performance_comparison.ipynb`
3. Run all cells to perform the complete analysis
4. Use the interactive monitoring controls to collect performance data

## 📊 What Gets Measured

### Performance Metrics
- **CPU Usage**: Percentage utilization per container
- **Memory Usage**: RAM consumption in MB and percentage
- **Resource Stability**: Standard deviation of usage over time
- **Application Health**: HTTP response availability
- **System Resources**: Overall host system metrics

### Analysis Features
- Real-time performance monitoring
- Interactive data collection controls
- Statistical analysis and rankings
- Comprehensive visualizations
- Export to CSV/JSON formats

## 🐳 Container Configuration

### Node.js Container
- **Base Image**: `node:18-alpine`
- **Port**: 3001
- **Package Manager**: npm
- **Health Check**: HTTP GET to `/`

### Deno Container  
- **Base Image**: `denoland/deno:1.37.0`
- **Port**: 3002
- **Package Manager**: deno (native)
- **Health Check**: HTTP GET to `/`

### Bun Container
- **Base Image**: `oven/bun:1.0.7` 
- **Port**: 3003
- **Package Manager**: bun (native)
- **Health Check**: HTTP GET to `/`

### Monitoring (moved to external repo)
The performance monitoring tooling (Jupyter notebook, Python monitoring script and Dockerfile) has been moved to a separate repository to keep this project focused on the runtime comparison.

Please visit the external monitoring repo for setup and usage:

https://github.com/Joeri-Abbo/docker-container-monitoring

That repository contains the monitoring Dockerfile, the `performance_monitor.py` script, the Jupyter notebook (`runtime_performance_comparison.ipynb`), and step-by-step instructions for collecting and visualizing performance data.

If you still have a `monitoring/` folder in this workspace it is a legacy copy — use the linked repo above for the up-to-date monitoring workflow.

## 📈 Performance Analysis Workflow

1. **Setup Phase**: Verify project structure and dependencies
2. **Container Health**: Check all containers are running and healthy
3. **Data Collection**: Monitor containers for specified duration
4. **Statistical Analysis**: Calculate means, standard deviations, rankings
5. **Visualization**: Generate comparative charts and graphs
6. **Insights**: Identify performance winners and efficiency patterns

## 🛠️ Manual Commands

### Build Individual Containers
```bash
# Node.js
docker build -t node-nextjs ./node-nextjs

# Deno  
docker build -t deno-nextjs ./deno-nextjs

# Bun
docker build -t bun-nextjs ./bun-nextjs

# Monitoring
The monitoring tooling is maintained in a separate repository; see https://github.com/Joeri-Abbo/docker-container-monitoring for build and run instructions.
```

### Run Performance Monitor Standalone
The performance monitor is now hosted in the external repo. Follow that project's README to build and run the monitoring container and the Jupyter notebook. Example usage and CLI options are documented there:

https://github.com/Joeri-Abbo/docker-container-monitoring

### Access Container Logs
```bash
docker-compose logs -f node-nextjs
docker-compose logs -f deno-nextjs  
docker-compose logs -f bun-nextjs
```

## 📊 Expected Results

Performance characteristics may vary based on:
- **Application Complexity**: Simple vs complex Next.js applications
- **System Resources**: Available CPU, memory, and I/O
- **Container Allocation**: Resource limits and sharing
- **Network Conditions**: Internal container networking

### Typical Performance Patterns:
- **Bun**: Often shows lower memory usage and faster startup
- **Deno**: Balanced performance with strong security model
- **Node.js**: Mature runtime with predictable resource usage

## 🔧 Customization

### Modify Monitoring Parameters
Edit `monitoring/performance_monitor.py`:
- Change monitoring interval
- Add custom metrics
- Modify container targets
- Adjust data export formats

### Customize Next.js Applications
Each runtime folder contains a complete Next.js application:
- Add routes in `src/app/`
- Modify `package.json` dependencies
- Update `next.config.js` settings
- Customize Dockerfile builds

### Extend Analysis
The Jupyter notebook can be extended with:
- Load testing integration
- Database performance metrics
- Network latency measurements
- Custom visualization types

## 🚨 Troubleshooting

### Containers Not Starting
```bash
# Check Docker daemon
docker info

# View container logs
docker-compose logs [service-name]

# Rebuild containers
docker-compose build --no-cache
```

### Performance Data Issues
```bash
# Check monitoring container logs
docker-compose logs monitoring

# Verify data directory
docker-compose exec monitoring ls -la /app/data/

# Restart monitoring
docker-compose restart monitoring
```

### Port Conflicts
If ports are already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "3001:3001"  # Change first number only
```

## 📝 License

This project is for educational and comparison purposes. Each runtime and framework maintains its own license terms.

## 🤝 Contributing

1. Fork the repository
2. Create performance tests for additional scenarios
3. Add support for more JavaScript runtimes
4. Improve visualization and analysis capabilities
5. Submit pull requests with detailed descriptions

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Node.js Performance Guide](https://nodejs.org/en/docs/guides/nodejs-performance)  
- [Deno Manual](https://deno.land/manual)
- [Bun Documentation](https://bun.sh/docs)
- [Docker Compose Reference](https://docs.docker.com/compose/)