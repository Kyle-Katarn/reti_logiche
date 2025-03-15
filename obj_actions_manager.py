import pygame
import GLOBAL_VARIABLES as GV

from visual_classes import *

class obj_action_manager():
    def __init__(self):
        # Main game loop
        self.running: bool = True
        # gestione spostamento gate
        self.selected_gate: VisualGate = None
        # gestione pin e crezione connessioni
        self.first_pin: VisualPin = None
        self.second_pin: VisualPin = None
        self.selected_pin: VisualPin = None
        self.is_first_pin_already_selected = False
        self.first_pin_type = None
        self.connection_being_created: VisualConnection = None
        # gestione azioni (cancellazione, copia, incolla) su oggetto
        # selected_gate
        self.selected_connection: VisualConnection = None
        self.gates_chosen_for_action_set: set[VisualGate] = set()
        self.are_gates_chosen_for_action_being_dragged: bool = False
        self.connections_chosen_for_action_set: set[VisualConnection] = set()

    def handle_event(self, event, keys_pressed, debug_prints=False):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #L'evento pygame.MOUSEBUTTONDOWN si attiva solo per un singolo frame quindi il for è chiamato 1 sola volta per pressione
            self.selected_pin = None
            self.selected_gate = None
            for gate in GV.GLOBAL_visual_gates: 
                self.selected_connection = gate.check_if_a_visual_connection_is_cicked(mouse_x, mouse_y)#*HAI PREMUTO SU UNA CONNESSIONE
                if((keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]) and self.selected_connection):
                    break

                self.selected_pin = gate.check_if_a_visual_pin_is_cicked(mouse_x, mouse_y)#*HAI PREMUTO SU UN PIN
                if(self.selected_pin):
                    break#check dei pin ha la precedenza

                if not self.selected_gate and gate.visual_gate_contains_point(mouse_x, mouse_y):#*HAI PREMUTO SU UN GATE
                    self.selected_gate = gate
                    break


            if not keys_pressed[pygame.K_LCTRL] and not keys_pressed[pygame.K_RCTRL]: #*CTRL non sta vendendo Premuto
                if(self.selected_pin): #was_mouse_button_up non è necessario, perchè BUTTONDOWN è attivo per un solo frame
                    if(not self.is_first_pin_already_selected):#* SELEZIONE 1^PIN
                        if debug_prints:
                            print("PRIMO pin selezionato con successo")
                        self.connection_being_created:VisualConnection = VisualConnection()
                        self.first_pin_type = self.selected_pin.type
                        self.connection_being_created.set_pin(self.selected_pin)
                        self.is_first_pin_already_selected = True

                    else:#* 1^pin è già stato selezionato; SELEZIONE 2^PIN
                        if(self.selected_pin.type == self.first_pin_type):
                            if debug_prints:
                                print("WARNING, you can't connect 2 inputs or 2 outputs")
                        else:
                            if debug_prints:
                                print("secondo pin selezionato con successo")
                            self.connection_being_created.set_pin(self.selected_pin)#todo setta collegamento logico se entrambi i pin sono != NULL
                            #self.connection_being_created.get_end_pin_visual_gate().visual_connections.add(self.connection_being_created)#todo non necessaria
                            self.connection_being_created.is_connection_finalized = True
                            self.connection_being_created = None #reset
                            self.is_first_pin_already_selected = False #reset
                            self.first_pin_type = None #reset

                else:#hai premuto sul vuoto o su un gate
                    if debug_prints:
                        print("hai premuto sul vuoto o su un gate")
                    self.connection_being_created = None #reset
                    self.is_first_pin_already_selected = False #reset
                    self.first_pin_type = None #reset
                
                if(self.selected_gate):#*START SPOSTAMENTO 1 GATE
                    #print(f"{mouse_x}, {mouse_y}")
                    self.selected_gate.visual_gate_start_drag(mouse_x, mouse_y)

            else:#* SELEZIONE E DESELEZIONE DI GATES E CONNESSIONI
                #print("CTRL STA VENENDO PREMUTO")
                self.connection_being_created = None #reset
                self.is_first_pin_already_selected = False #reset
                self.first_pin_type = None #reset
                if(self.selected_connection):
                    if debug_prints:
                        print("CTRL click su una connessione")
                    if(not self.selected_connection in self.connections_chosen_for_action_set):
                        self.connections_chosen_for_action_set.add(self.selected_connection)
                        self.selected_connection.is_self_in_connections_chosen_for_action_set = True
                    else:
                        self.connections_chosen_for_action_set.remove(self.selected_connection)
                        self.selected_connection.is_self_in_connections_chosen_for_action_set = False
                elif(self.selected_gate):
                    if debug_prints:
                        print("CTRL click su un gate")
                    if(not self.selected_gate in self.gates_chosen_for_action_set):
                        self.gates_chosen_for_action_set.add(self.selected_gate)
                        self.selected_gate.color = GV.GREEN
                    else:
                        self.gates_chosen_for_action_set.remove(self.selected_gate)
                        self.selected_gate.color = GV.LIGHTBLUE
                else:
                    if debug_prints:
                        print("CTRL click sul vuoto")
                    for vg in self.gates_chosen_for_action_set:
                        vg.color = GV.LIGHTBLUE
                    self.gates_chosen_for_action_set.clear()
                    for vc in self.connections_chosen_for_action_set:
                        vc.is_self_in_connections_chosen_for_action_set = False
                    self.connections_chosen_for_action_set.clear()


            if(False):
                print("STATUS:")
                print(f"selected_pin: {self.selected_pin}")
                print(f"is_first_pin_already_selected: {self.is_first_pin_already_selected}")
                print(f"first_pin_type: {self.first_pin_type}")
                print(f"connection_being_created: {self.connection_being_created}")
                print("")
            
        elif event.type == pygame.MOUSEBUTTONUP:
            if debug_prints:
                print("mouse button up")
            if self.selected_gate:#*END SPOSTAMENTO 1 GATE
                self.selected_gate.visual_gate_end_drag()
                self.selected_gate = None

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:  # *START/END SPOSTAMENTO N GATES in self.gates_chosen_for_action_set
            if debug_prints:
                print("K_m")
            self.are_gates_chosen_for_action_being_dragged = not self.are_gates_chosen_for_action_being_dragged 
            for vg in self.gates_chosen_for_action_set.copy():
                if(self.are_gates_chosen_for_action_being_dragged):
                    vg.visual_gate_start_drag(mouse_x,mouse_y)
                else:
                    vg.visual_gate_end_drag()
                    for vg in self.gates_chosen_for_action_set:#reset
                        vg.color = GV.LIGHTBLUE
                    self.gates_chosen_for_action_set.clear()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:  #* CANCELLAZIONE GATES, CONNESSIONI
            for vg in self.gates_chosen_for_action_set:
                GV.GLOBAL_visual_gates.remove(vg)
                vg.delete_internal_logic_gate()

            for vc in self.connections_chosen_for_action_set:
                vc.remove_self()
                vc.unconnect_logic_pins()
                pass
            self.gates_chosen_for_action_set.clear()
            self.connections_chosen_for_action_set.clear()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            if debug_prints:
                print("K_c")
            import copy
            copied_gates:set[VisualGate] = copy.deepcopy(self.gates_chosen_for_action_set)
            for vc in self.gates_chosen_for_action_set:
                vc.color = GV.LIGHTBLUE
            self.gates_chosen_for_action_set.clear()
            self.gates_chosen_for_action_set.update(copied_gates)
            for vc in self.gates_chosen_for_action_set:
                vc.x+=30
                vc.y+=30
            GV.GLOBAL_visual_gates.extend(copied_gates)

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if(self.connection_being_created != None): #*SPOSTAMENTO MOUSE self.connection_being_created
                self.connection_being_created.auto_update_connection()
                if(self.first_pin_type == "out"):#spostalo interno a classe pin?
                    self.connection_being_created.set_coordinates(end=(mouse_x,mouse_y))
                else:
                    self.connection_being_created.set_coordinates(start=(mouse_x,mouse_y))
            
            if self.selected_gate:#* SPOSTAMENTO MOUSE 1 GATE
                self.selected_gate.visual_gate_update_position(mouse_x, mouse_y)
            if self.are_gates_chosen_for_action_being_dragged:#*SPOSTAMENTO MOUSE N GATES
                for vg in self.gates_chosen_for_action_set:
                    vg.visual_gate_update_position(mouse_x,mouse_y)

    
    def draw(self, screen):
        if(self.connection_being_created != None):
            self.connection_being_created.draw(screen=screen)