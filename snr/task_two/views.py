import threading
import time

from flask import jsonify

from snr.task_two.handler import BasicQueueService, WorkQueueService, PubSubService
from snr.task_two import BP_TASK_TWO


@BP_TASK_TWO.route('/v1/basic_queue', methods=['GET'])
def basic_queue():
    basic_queue_service = BasicQueueService()
    basic_queue_service.send_message()

    def receive_basic_queue():
        basic_queue_service.receive_messages()
        time.sleep(5)
        basic_queue_service.close()

    threading.Thread(target=receive_basic_queue).start()

    return jsonify({
        "status": "Basic Queue Done, check terminal for received messages"
    })


@BP_TASK_TWO.route('/v1/work_queue', methods=['GET'])
def work_queue():
    work_queue_service = WorkQueueService()
    for i in range(1, 6):
        work_queue_service.send_message(f"Task {i}")

    def receive_work_queue():
        work_queue_service.receive_messages()
        time.sleep(5)
        work_queue_service.close()

    threading.Thread(target=receive_work_queue).start()

    return jsonify({
        "status": "Work Queue Done, check terminal for received messages"
    })


@BP_TASK_TWO.route('/v1/pub_sub', methods=['GET'])
def pub_sub():
    pub_sub_service = PubSubService()
    pub_sub_service.publish_message()

    def receive_pub_sub():
        pub_sub_service.subscribe()
        time.sleep(5)
        pub_sub_service.close()

    threading.Thread(target=receive_pub_sub).start()

    return jsonify({
        "status": "Pub Sub Done, check terminal for received messages"
    })
