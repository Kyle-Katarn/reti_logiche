import pygame
import GLOBAL_VARIABLES as GV

class ButtonClass:
    def __init__(self, x, y, width=100, height=50, text="Button"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GV.LIGHTBLUE
        self.hover_color = GV.YELLOW
        self.font = pygame.font.Font(None, 24)
        self.is_hovered = False
        self.was_mouse_button_up = True

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, GV.BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered and self.was_mouse_button_up:
            self.button_function()
            self.was_mouse_button_up = False
        elif event.type == pygame.MOUSEBUTTONUP:
            self.was_mouse_button_up = True

    def button_function(self):
        print(f"Button {self.text} clicked")


class NextFrameButton(ButtonClass):
    def __init__(self):
        super().__init__(x=210, y=GV.SCREEN_HEIGHT-60, width=150, height=50, text="Next Frame")
        

class PreviousFrameButton(ButtonClass):
    def __init__(self):
        super().__init__(x=10, y=GV.SCREEN_HEIGHT-60, width=150, height=50, text="Previous Frame")

class PlaySimulationButton(ButtonClass):
    def __init__(self):
        super().__init__(x=410, y=GV.SCREEN_HEIGHT-60, width=150, height=50, text="Play Simulation")


class InputField(ButtonClass):
    def __init__(self):
        super().__init__(610, GV.SCREEN_HEIGHT-60, 150, 50, text="")
        self.active = False
        self.input_text = ""
        self.color_inactive = GV.LIGHTBLUE
        self.color_active = GV.YELLOW
        self.color = self.color_inactive

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.was_mouse_button_up:
            # If the user clicked on the input box
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box
            self.color = self.color_active if self.active else self.color_inactive
            self.was_mouse_button_up = False

        elif event.type == pygame.MOUSEBUTTONUP:
            self.was_mouse_button_up = True            

        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.input_text)
                    self.input_text = ""
                    #generate_more_simulation_frames(str(input_text))
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

    def draw(self, screen):
        # Render the current text
        text_surface = self.font.render(self.input_text, True, GV.BLACK)
        # Resize the box if the text is too long
        width = max(200, text_surface.get_width() + 10)
        self.rect.w = width
        # Blit the text
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect
        pygame.draw.rect(screen, self.color, self.rect, 2)

