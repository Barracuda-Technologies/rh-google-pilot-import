from eventmanager import Evt
from .gpilot import Gpilot

def initialize(rhapi):
    gpilot = Gpilot(rhapi)
    rhapi.events.on(Evt.STARTUP, gpilot.init_plugin)