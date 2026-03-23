# helpers.py
import logging
import time
from retrying import retry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def safe_get(request_func, *args, **kwargs):
    response = request_func(*args, **kwargs)
    response.raise_for_status()
    return response

def exponential_backoff_retry(func, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            wait = 2 ** attempt
            logging.warning(f"Attempt {attempt+1} failed: {e}. Retrying in {wait}s...")
            time.sleep(wait)
    logging.error("Max retries exceeded.")
    return None