import psutil
import os

class MemoryTracker:
    def __init__(self):
        self.memory_usage_array = []

    def update_memory_usage_array(self):
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        memory_usage_in_mb = memory_info.rss / (1024 * 1024)
        self.memory_usage_array.append(memory_usage_in_mb)

    def calculate_average_memory_usage(self):
        if len(self.memory_usage_array) == 0:
            return
        total = sum(self.memory_usage_array)
        average = total / len(self.memory_usage_array)
        result_string = f"{average:.2f} MB"
        return result_string