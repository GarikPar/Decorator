import random
import time

def retry(exceptions, tries=3, delay=2, backoff=2, logger=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            global start_time
            start_time = time.time()
            local_tries = tries
            local_delay = delay
            while local_tries > 0:
                try:
                    result = func(*args, **kwargs)
                    return result
                except exceptions as e:
                    local_tries -= 1
                    if local_tries == 0:
                        raise e
                    time.sleep(local_delay)
                    local_delay *= backoff
                    if logger:
                        logger.exception(f"Retrying in {local_delay} seconds...")
        return wrapper
    return decorator

@retry(Exception, tries=3, delay=2, backoff=2, logger=None)
def random_numbers_interval(p, q):
    random_number = random.random()
    if random_number < p:
        raise Exception('less than lower bound')
    if random_number > q:
        raise Exception('greater than upper bound')
    else:
        end_time = time.time()
        print(f"Code successfully work and it lasts {end_time - start_time}")

# Example usage:
try:
    random_numbers_interval(0.1, 0.7)
except Exception as e:
    print(f"Caught exception: {e}")