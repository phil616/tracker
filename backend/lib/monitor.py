import psutil

class SystemStatusMonitor:
    def __init__(self):
        self.cpu_percent = psutil.cpu_percent()
        self.memory = psutil.virtual_memory()
        self.disk = psutil.disk_usage('/')

    def get_status(self)->dict:
        return {
            "cpu_percent": self.cpu_percent,
            "memory_total": self.memory.total,
            "memory_used": self.memory.used,
            "memory_percent": self.memory.percent,
            "disk_total": self.disk.total,
            "disk_used": self.disk.used,
            "disk_percent": self.disk.percent
        }
    

monitor = SystemStatusMonitor()
