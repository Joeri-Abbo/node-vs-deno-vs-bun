import docker
import psutil
import time
import json
import pandas as pd
from datetime import datetime
import logging
import requests
from typing import Dict, List, Optional
import threading
import signal
import sys

class PerformanceMonitor:
    def __init__(self, interval: int = 10):
        """
        Initialize the performance monitor
        
        Args:
            interval: Monitoring interval in seconds
        """
        self.interval = interval
        self.client = docker.from_env()
        self.data = []
        self.running = False
        self.containers = {
            'node-nextjs-app': 'http://localhost:3001',
            'deno-nextjs-app': 'http://localhost:3002',
            'bun-nextjs-app': 'http://localhost:3003'
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info("Received shutdown signal. Stopping monitoring...")
        self.running = False
        self.save_data()
        sys.exit(0)
    
    def get_container_stats(self, container_name: str) -> Optional[Dict]:
        """
        Get container statistics including CPU and memory usage
        
        Args:
            container_name: Name of the container to monitor
            
        Returns:
            Dictionary containing container stats or None if container not found
        """
        try:
            container = self.client.containers.get(container_name)
            stats = container.stats(stream=False)
            
            # Calculate CPU usage percentage
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                       stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                          stats['precpu_stats']['system_cpu_usage']
            
            cpu_percent = 0.0
            if system_delta > 0:
                cpu_percent = (cpu_delta / system_delta) * \
                             len(stats['cpu_stats']['cpu_usage']['percpu_usage']) * 100
            
            # Calculate memory usage
            memory_usage = stats['memory_stats']['usage']
            memory_limit = stats['memory_stats']['limit']
            memory_percent = (memory_usage / memory_limit) * 100
            
            return {
                'container_name': container_name,
                'cpu_percent': round(cpu_percent, 2),
                'memory_usage_mb': round(memory_usage / (1024 * 1024), 2),
                'memory_percent': round(memory_percent, 2),
                'status': container.status,
                'timestamp': datetime.now().isoformat()
            }
        except docker.errors.NotFound:
            self.logger.warning(f"Container {container_name} not found")
            return None
        except Exception as e:
            self.logger.error(f"Error getting stats for {container_name}: {e}")
            return None
    
    def check_container_health(self, container_name: str, url: str) -> bool:
        """
        Check if container is responding to HTTP requests
        
        Args:
            container_name: Name of the container
            url: URL to check
            
        Returns:
            True if container is healthy, False otherwise
        """
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_system_stats(self) -> Dict:
        """
        Get overall system statistics
        
        Returns:
            Dictionary containing system stats
        """
        return {
            'system_cpu_percent': psutil.cpu_percent(interval=1),
            'system_memory_percent': psutil.virtual_memory().percent,
            'system_memory_available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
            'timestamp': datetime.now().isoformat()
        }
    
    def collect_metrics(self):
        """Collect metrics from all containers and system"""
        timestamp = datetime.now()
        metrics = {
            'timestamp': timestamp.isoformat(),
            'system': self.get_system_stats(),
            'containers': {}
        }
        
        for container_name, url in self.containers.items():
            container_stats = self.get_container_stats(container_name)
            if container_stats:
                container_stats['healthy'] = self.check_container_health(container_name, url)
                metrics['containers'][container_name] = container_stats
        
        self.data.append(metrics)
        self.logger.info(f"Collected metrics at {timestamp}")
        
        # Log current stats
        for container_name, stats in metrics['containers'].items():
            if stats:
                self.logger.info(
                    f"{container_name}: CPU: {stats['cpu_percent']}%, "
                    f"Memory: {stats['memory_usage_mb']}MB ({stats['memory_percent']}%), "
                    f"Healthy: {stats['healthy']}"
                )
    
    def save_data(self, filename: Optional[str] = None):
        """
        Save collected data to JSON and CSV files
        
        Args:
            filename: Optional custom filename (without extension)
        """
        if not self.data:
            self.logger.warning("No data to save")
            return
        
        if filename is None:
            filename = f"performance_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save as JSON
        json_path = f"/app/data/{filename}.json"
        with open(json_path, 'w') as f:
            json.dump(self.data, f, indent=2)
        
        # Convert to pandas DataFrame and save as CSV
        flattened_data = []
        for entry in self.data:
            base_row = {
                'timestamp': entry['timestamp'],
                'system_cpu_percent': entry['system']['system_cpu_percent'],
                'system_memory_percent': entry['system']['system_memory_percent'],
                'system_memory_available_gb': entry['system']['system_memory_available_gb']
            }
            
            for container_name, stats in entry['containers'].items():
                if stats:
                    row = base_row.copy()
                    row.update({
                        'container_name': container_name,
                        'container_cpu_percent': stats['cpu_percent'],
                        'container_memory_usage_mb': stats['memory_usage_mb'],
                        'container_memory_percent': stats['memory_percent'],
                        'container_healthy': stats['healthy'],
                        'container_status': stats['status']
                    })
                    flattened_data.append(row)
        
        if flattened_data:
            df = pd.DataFrame(flattened_data)
            csv_path = f"/app/data/{filename}.csv"
            df.to_csv(csv_path, index=False)
            
            self.logger.info(f"Data saved to {json_path} and {csv_path}")
            return csv_path, json_path
        
        return None, json_path
    
    def start_monitoring(self, duration: Optional[int] = None):
        """
        Start the monitoring process
        
        Args:
            duration: Optional duration in seconds. If None, runs indefinitely
        """
        self.running = True
        start_time = time.time()
        
        self.logger.info(f"Starting performance monitoring with {self.interval}s interval")
        if duration:
            self.logger.info(f"Monitoring will run for {duration} seconds")
        
        try:
            while self.running:
                self.collect_metrics()
                
                if duration and (time.time() - start_time) >= duration:
                    self.logger.info("Monitoring duration completed")
                    break
                
                time.sleep(self.interval)
        
        except KeyboardInterrupt:
            self.logger.info("Monitoring interrupted by user")
        finally:
            self.running = False
            self.save_data()
    
    def get_latest_data(self) -> Optional[Dict]:
        """Get the most recent collected data"""
        return self.data[-1] if self.data else None
    
    def get_dataframe(self) -> pd.DataFrame:
        """Convert collected data to pandas DataFrame"""
        if not self.data:
            return pd.DataFrame()
        
        flattened_data = []
        for entry in self.data:
            base_row = {
                'timestamp': pd.to_datetime(entry['timestamp']),
                'system_cpu_percent': entry['system']['system_cpu_percent'],
                'system_memory_percent': entry['system']['system_memory_percent'],
                'system_memory_available_gb': entry['system']['system_memory_available_gb']
            }
            
            for container_name, stats in entry['containers'].items():
                if stats:
                    row = base_row.copy()
                    row.update({
                        'container_name': container_name,
                        'container_cpu_percent': stats['cpu_percent'],
                        'container_memory_usage_mb': stats['memory_usage_mb'],
                        'container_memory_percent': stats['memory_percent'],
                        'container_healthy': stats['healthy'],
                        'container_status': stats['status']
                    })
                    flattened_data.append(row)
        
        return pd.DataFrame(flattened_data)

def main():
    """Main function to run the performance monitor"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor Next.js runtime performance')
    parser.add_argument('--interval', type=int, default=10, 
                       help='Monitoring interval in seconds (default: 10)')
    parser.add_argument('--duration', type=int, default=None,
                       help='Monitoring duration in seconds (default: infinite)')
    
    args = parser.parse_args()
    
    monitor = PerformanceMonitor(interval=args.interval)
    monitor.start_monitoring(duration=args.duration)

if __name__ == "__main__":
    main()