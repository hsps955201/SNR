import threading
import time

from flask import jsonify
from queue import Queue

import config

from snr.task_one import BP_TASK_ONE
from snr.task_one.handler import producer, consumer
from snr.utils.logging import logger


shared_queue = Queue(maxsize=config.QUEUE_MAX_SIZE)
lock = threading.Lock()

produced_items = []
consumed_items = []


@BP_TASK_ONE.route('/v1/multi_threading', methods=['GET'])
def multi_threading():
    producer_thread = threading.Thread(
        target=producer, args=(shared_queue, produced_items, lock))
    consumer_thread = threading.Thread(
        target=consumer, args=(shared_queue, consumed_items, lock))

    producer_thread.start()
    consumer_thread.start()

    time.sleep(config.RUN_TIME)

    producer_thread.join(timeout=1)
    consumer_thread.join(timeout=1)

    print("produced_items", produced_items)
    print("consumed_items", consumed_items)
    logger.info(f"produced_items: {produced_items}")
    logger.info(f"consumed_items: {consumed_items}")

    return jsonify({
        "produced_items": produced_items,
        "consumed_items": consumed_items
    })
