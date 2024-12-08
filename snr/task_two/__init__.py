
from flask import Blueprint

BP_TASK_TWO = Blueprint("task2", __name__)


def register_views():
    import snr.task_two.views


register_views()
