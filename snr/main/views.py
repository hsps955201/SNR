from snr.main import BP_MAIN
from snr.utils.logging import logger


@BP_MAIN.route('/', methods=['GET'])
def hello():
    default_message = "Welcome to the SNR API"
    print(default_message)
    logger.info(default_message)

    return default_message
