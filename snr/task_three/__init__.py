
from flask import Blueprint

BP_TASK_THREE = Blueprint("task3", __name__)


def register_views():
    import snr.task_three.views


register_views()
