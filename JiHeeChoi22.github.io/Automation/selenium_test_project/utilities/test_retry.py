import logging
import time
import functools

class TestRetry:
    @staticmethod
    def retry_test(max_attempts=3, wait_time=1):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_attempts - 1:
                            raise
                        logging.warning(f"테스트 실패, 재시도 중... ({attempt + 1}/{max_attempts})")
                        time.sleep(wait_time)
            return wrapper
        return decorator 