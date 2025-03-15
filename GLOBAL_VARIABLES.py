from typing import TYPE_CHECKING
from reti_logiche import *
if TYPE_CHECKING:
    from visual_classes import VisualGate


BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHTBLUE = (173, 216, 230)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

GLOBAL_visual_gates:set["VisualGate"] = []
considered_gates=[not1,not2]