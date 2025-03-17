import pygame
from math import sqrt
from reti_logiche import *
from ui_elements import *
import GLOBAL_VARIABLES as GV
from visual_classes import *
from obj_actions_manager import *
from auto_placement import *




# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((GV.SCREEN_WIDTH, GV.SCREEN_HEIGHT))
pygame.display.set_caption("Logic Gates Visualizer")

considered_gates=[prova]#??? GV.??
GV.GLOBAL_visual_gates = auto_placement(considered_gates=considered_gates)


UI_ELEMENTS_SET:set[ButtonClass] = set()
next_frame_button = NextFrameButton()
previous_frame_button = PreviousFrameButton()
play_simulation_button = PlaySimulationButton()
input_field = InputField()
UI_ELEMENTS_SET.add(next_frame_button)
UI_ELEMENTS_SET.add(previous_frame_button)
UI_ELEMENTS_SET.add(play_simulation_button)
UI_ELEMENTS_SET.add(input_field)

obj_action_manager_instance:"obj_action_manager" = obj_action_manager()

running:bool = True
while running:
    keys_pressed = pygame.key.get_pressed()#premute in un dato frame, dura N frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        obj_action_manager_instance.handle_event(event, keys_pressed)

        for button in UI_ELEMENTS_SET:
            button.handle_event(event)

    
    screen.fill(GV.WHITE)

    obj_action_manager_instance.draw(screen)
    
    # Draw all gates
    for visual_gate in GV.GLOBAL_visual_gates.copy():
        visual_gate.draw(screen)

    # draw all buttons
    for button in UI_ELEMENTS_SET:
        button.draw(screen)

    pygame.display.flip()

pygame.quit()
