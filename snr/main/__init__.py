
from flask import Blueprint

BP_MAIN = Blueprint("/", __name__)


def register_views():
    import snr.main.views


register_views()
