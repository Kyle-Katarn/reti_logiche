from gui import *
from visual_classes import *

#gestione spostamento gate
selected_gate:VisualGate = None
#gestione pin e crezione connessioni
first_pin:VisualPin = None
second_pin:VisualPin = None
selected_pin:VisualPin = None
is_first_pin_already_selected = False
first_pin_type = None
#gestione azioni (cancellazione, copia, incolla) su oggetto
#selected_gate
selected_connection:VisualConnection = None
gates_chosen_for_action_set:set[VisualGate] = set()
are_gates_chosen_for_action_being_dragged:bool = False
connections_chosen_for_action_set:set[VisualConnection] = set()

def manage_logic_obj_event(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #L'evento pygame.MOUSEBUTTONDOWN si attiva solo per un singolo frame quindi il for è chiamato 1 sola volta per pressione
        selected_pin = None
        selected_gate = None
        for gate in GLOBAL_visual_gates: 
            selected_connection = gate.check_if_a_visual_connection_is_cicked(mouse_x, mouse_y)#*HAI PREMUTO SU UNA CONNESSIONE
            if((keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]) and selected_connection):
                break

            selected_pin = gate.check_if_a_visual_pin_is_cicked(mouse_x, mouse_y)#*HAI PREMUTO SU UN PIN
            if(selected_pin):
                break#check dei pin ha la precedenza

            if not selected_gate and gate.visual_gate_contains_point(mouse_x, mouse_y):#*HAI PREMUTO SU UN GATE
                selected_gate = gate
                break


        if not keys_pressed[pygame.K_LCTRL] and not keys_pressed[pygame.K_RCTRL]: #*CTRL non sta vendendo Premuto
            if(selected_pin): #was_mouse_button_up non è necessario, perchè BUTTONDOWN è attivo per un solo frame
                if(not is_first_pin_already_selected):#* SELEZIONE 1^PIN
                    print("PRIMO pin selezionato con successo")
                    connection_being_created:VisualConnection = VisualConnection()
                    first_pin_type = selected_pin.type
                    connection_being_created.set_pin(selected_pin)
                    is_first_pin_already_selected = True

                else:#* 1^pin è già stato selezionato; SELEZIONE 2^PIN
                    if(selected_pin.type == first_pin_type):
                        print("WARNING, you can't connect 2 inputs or 2 outputs")
                    else:
                        print("secondo pin selezionato con successo")
                        connection_being_created.set_pin(selected_pin)#todo setta collegamento logico se entrambi i pin sono != NULL
                        #connection_being_created.get_end_pin_visual_gate().visual_connections.add(connection_being_created)#todo non necessaria
                        connection_being_created.is_connection_finalized = True
                        connection_being_created = None #reset
                        is_first_pin_already_selected = False #reset
                        first_pin_type = None #reset

            else:#hai premuto sul vuoto o su un gate
                print("hai premuto sul vuoto o su un gate")
                connection_being_created = None #reset
                is_first_pin_already_selected = False #reset
                first_pin_type = None #reset
            
            if(selected_gate):#*START SPOSTAMENTO 1 GATE
                #print(f"{mouse_x}, {mouse_y}")
                selected_gate.visual_gate_start_drag(mouse_x, mouse_y)

        else:#* SELEZIONE E DESELEZIONE DI GATES E CONNESSIONI
            #print("CTRL STA VENENDO PREMUTO")
            connection_being_created = None #reset
            is_first_pin_already_selected = False #reset
            first_pin_type = None #reset
            if(selected_connection):
                print("CTRL click su una connessione")
                if(not selected_connection in connections_chosen_for_action_set):
                    connections_chosen_for_action_set.add(selected_connection)
                    selected_connection.is_self_in_connections_chosen_for_action_set = True
                else:
                    connections_chosen_for_action_set.remove(selected_connection)
                    selected_connection.is_self_in_connections_chosen_for_action_set = False
            elif(selected_gate):
                print("CTRL click su un gate")
                if(not selected_gate in gates_chosen_for_action_set):
                    gates_chosen_for_action_set.add(selected_gate)
                    selected_gate.color = GREEN
                else:
                    gates_chosen_for_action_set.remove(selected_gate)
                    selected_gate.color = LIGHTBLUE
            else:
                print("CTRL click sul vuoto")
                for vg in gates_chosen_for_action_set:
                    vg.color = LIGHTBLUE
                gates_chosen_for_action_set.clear()
                for vc in connections_chosen_for_action_set:
                    vc.is_self_in_connections_chosen_for_action_set = False
                connections_chosen_for_action_set.clear()


        if(False):
            print("STATUS:")
            print(f"selected_pin: {selected_pin}")
            print(f"is_first_pin_already_selected: {is_first_pin_already_selected}")
            print(f"first_pin_type: {first_pin_type}")
            print(f"connection_being_created: {connection_being_created}")
            print("")
        
    elif event.type == pygame.MOUSEBUTTONUP:
        print("mouse button up")
        if selected_gate:#*END SPOSTAMENTO 1 GATE
            selected_gate.visual_gate_end_drag()
            selected_gate = None

    elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:  # *START/END SPOSTAMENTO N GATES in gates_chosen_for_action_set
        print("K_m")
        are_gates_chosen_for_action_being_dragged = not are_gates_chosen_for_action_being_dragged 
        for vg in gates_chosen_for_action_set.copy():
            if(are_gates_chosen_for_action_being_dragged):
                vg.visual_gate_start_drag(mouse_x,mouse_y)
            else:
                vg.visual_gate_end_drag()
                for vg in gates_chosen_for_action_set:#reset
                    vg.color = LIGHTBLUE
                gates_chosen_for_action_set.clear()

    elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:  #* CANCELLAZIONE GATES, CONNESSIONI
        for vg in gates_chosen_for_action_set:
            GLOBAL_visual_gates.remove(vg)
            vg.delete_internal_logic_gate()

        for vc in connections_chosen_for_action_set:
            vc.remove_self()
            vc.unconnect_logic_pins()
            pass
        gates_chosen_for_action_set.clear()
        connections_chosen_for_action_set.clear()

    elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
        print("K_c")
        import copy
        copied_gates:set[VisualGate] = copy.deepcopy(gates_chosen_for_action_set)
        for vc in gates_chosen_for_action_set:
            vc.color = LIGHTBLUE
        gates_chosen_for_action_set.clear()
        gates_chosen_for_action_set.update(copied_gates)
        for vc in gates_chosen_for_action_set:
            vc.x+=30
            vc.y+=30
        GLOBAL_visual_gates.extend(copied_gates)

    elif event.type == pygame.MOUSEMOTION:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if(connection_being_created != None): #*SPOSTAMENTO MOUSE connection_being_created
            connection_being_created.auto_update_connection()
            if(first_pin_type == "out"):#spostalo interno a classe pin?
                connection_being_created.set_coordinates(end=(mouse_x,mouse_y))
            else:
                connection_being_created.set_coordinates(start=(mouse_x,mouse_y))
        
        if selected_gate:#* SPOSTAMENTO MOUSE 1 GATE
            selected_gate.visual_gate_update_position(mouse_x, mouse_y)
        if are_gates_chosen_for_action_being_dragged:#*SPOSTAMENTO MOUSE N GATES
            for vg in gates_chosen_for_action_set:
                vg.visual_gate_update_position(mouse_x,mouse_y)