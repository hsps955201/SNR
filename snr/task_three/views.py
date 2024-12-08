from flask import request, jsonify
from snr.task_three import BP_TASK_THREE
from snr.utils.logging import logger


@BP_TASK_THREE.route('/v1/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'World')
    print(f"Hello, {name}!")
    logger.info(f"Hello, {name}!")

    return jsonify({'message': f'Hello, {name}!'})
