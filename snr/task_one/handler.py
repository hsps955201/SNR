import time
import random

import config

from snr.utils.logging import logger


def producer(shared_queue, produced_items, lock):
    for _ in range(config.EPOCHS):
        time.sleep(config.PRODUCER_INTERVAL)
        item = random.randint(1, config.RANDOM_RANGE)
        with lock:
            if not shared_queue.full():
                shared_queue.put(item)
                produced_items.append(item)
                print(f'Produced: {item}')
                logger.info(f'Produced: {item}')


def consumer(shared_queue, consumed_items, lock):
    for _ in range(config.EPOCHS):
        time.sleep(config.CONSUMER_INTERVAL)
        with lock:
            if not shared_queue.empty():
                item = shared_queue.get()
                consumed_items.append(item)
                print(f'Consumed: {item}')
                logger.info(f'Consumed: {item}')
