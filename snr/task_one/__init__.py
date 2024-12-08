
from flask import Blueprint

BP_TASK_ONE = Blueprint("task1", __name__)


def register_views():
    import snr.task_one.views


register_views()
