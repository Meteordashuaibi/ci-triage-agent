import time

def retry_with_backoff(func, max_retries=3, base_delay=1.0, max_delay=60.0):
    for attempt in range(max_retries):
        try:
            result = func()
            return result
        except Exception as e:
            wait = min(base_delay * (2 ** attempt), max_delay)
            print(f"Attempt {attempt + 1} failed. Retrying in {wait:.1f}s...")
            time.sleep(wait)
    raise Exception(f"All {max_retries} retries failed")
call_count = 0

def fake_api():
    global call_count
    call_count += 1
    if call_count < 3:
        raise Exception("API failed")
    return "success"
result = retry_with_backoff(fake_api)
print(result)