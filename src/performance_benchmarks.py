import time
import logging
import psutil
import os
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PerfMonitor")
def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        logger.info(f"Function {func.__name__} took {duration:.4f} seconds to complete.")
        return result
    return wrapper
class SystemBenchmark:
    @staticmethod
    def get_memory_usage():
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info().rss / (1024 * 1024)
        return mem_info
    @staticmethod
    def run_inference_benchmark(predict_fn, sample_df, iterations=5):
        logger.info(f"Starting inference benchmark for {iterations} iterations...")
        times = []
        for i in range(iterations):
            start = time.perf_counter()
            predict_fn(sample_df)
            times.append(time.perf_counter() - start)
        avg_time = sum(times) / iterations
        logger.info(f"Average Inference Latency: {avg_time:.4f}s")
        return avg_time
    @staticmethod
    def log_resource_snapshot():
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = SystemBenchmark.get_memory_usage()
        logger.info(f"Resource Snapshot - CPU: {cpu_usage}%, MEM: {mem_usage:.2f}MB")
if __name__ == "__main__":
    SystemBenchmark.log_resource_snapshot()
