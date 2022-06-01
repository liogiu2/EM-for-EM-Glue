import os
import sys
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'EV_PDDL'))
from platform_communication import PlatformCommunication
import time
import jsonpickle
from ev_pddl.PDDL import PDDL_Parser
from ev_pddl.world_state import WorldState
from ev_pddl.action import Action
import input_timeout
import threading
import json
import debugpy

class ExperienceManager:

    PDDL_domain_text = ""
    PDDL_problem_text = ""

    def __init__(self) -> None:
        self.platform_communication = PlatformCommunication()
        self._PDDL_parser = PDDL_Parser()

    def start_platform_communication(self):
        """
        This method is used to start the communication with the platform using the communication protocol.
        """
        print("Starting platform communication")
        self.wait_platform_online()
        #Handshake -- Phase 1
        print("Handshake -- Phase 1")
        message = self.platform_communication.get_handshake_message("PHASE_1", "message_1") + " Experience Manager"
        response = self.platform_communication.send_message(message, inizialization = True)
        if response is None:
            raise Exception("Error: Communication with platform failed.")
        if response['text'] == self.platform_communication.get_handshake_message("PHASE_1", "message_2"):
            print("Handshake -- phase 1 successful.")
        else:
            raise Exception("Error: Received unexpected message: " + response['text'])
        #Handshake -- Phase 3
        print("Handshake -- Phase 3")
        print("Waiting for phase 3 to start")
        self.wait_phase_3_start()
        print("Phase 3 started")
        message = self.platform_communication.get_handshake_message("PHASE_3", "message_5")
        print("Sending message: " + message)
        response = self.platform_communication.send_message(message, inizialization = True)
        if response is None:
            raise Exception("Error: Communication with platform failed.")
        if response['text'] == self.platform_communication.get_handshake_message("PHASE_3", "message_7"):
            self.PDDL_domain_text = str(response['domain'])
            print("Domain received successfully")
            self.PDDL_problem_text = str(response['problem'])
            print("Problem received successfully")
            print("Handshake -- phase 3 successful.")
        else:
            raise Exception("Error: Received unexpected message: " + response['text'])
        #Handshake -- Phase 4
        print("Handshake -- Phase 4")
        message = self.platform_communication.get_handshake_message("PHASE_4", "message_8")
        response = self.platform_communication.send_message(message, inizialization = True)
        if response is None:
            raise Exception("Error: Communication with platform failed.")
        if response['text'] == self.platform_communication.get_handshake_message("PHASE_4", "message_10"):
            self.platform_communication.receive_message_link = response['get_message_url'].replace("/", "")
            print("Receive message link received: /" + self.platform_communication.receive_message_link)
            self.platform_communication.send_message_link = response['add_message_url'].replace("/", "")
            print("Send message link received: /" + self.platform_communication.send_message_link)
            print("Handshake -- phase 4 successful.")
        else:
            raise Exception("Error: Received unexpected message: " + response['text'])
    
    def wait_platform_online(self):
        """
        This method is used to wait until the platform is online.
        """
        while not self.platform_communication.is_platform_online():
            time.sleep(1)
    
    def wait_phase_3_start(self):
        """
        This method is used to wait until the platform starts the phase 3.
        """
        while self.platform_communication.get_handshake_phase() != "PHASE_3":
            time.sleep(0.1)

    def main_loop(self):
        """
        This is the main loop of the experience manager.
        """
        self.platform_communication.start_receiving_messages()
        # debugpy.listen(5678)
        # debugpy.wait_for_client()
        self.domain = self._PDDL_parser.parse_domain(domain_str = self.PDDL_domain_text)
        # self.domain = self._PDDL_parser.parse_domain(domain_filename="domain.pddl")
        print("Domain parsed correcly")
        self.problem = self._PDDL_parser.parse_problem(problem_str = self.PDDL_problem_text)
        # self.problem = self._PDDL_parser.parse_problem(problem_filename="problem.pddl")
        print("Problem parsed correcly")
        self.environment_state = WorldState()
        self.environment_state.create_worldstate_from_problem(problem = self.problem, domain=self.domain)
        print("Starting normal communication...")
        print("Press something to start the action builder...")
        thread = None
        while True:
            message = self.platform_communication.get_received_message()
            if message is not None:
                changed_relations = []
                for item in message:
                    rel = jsonpickle.decode(item['text'])
                    changed_relations.append(rel)
                if thread is None or thread.is_alive() == False:
                    print("Received message: " + str(changed_relations))
                self.update_environment_state(changed_relations)
            if thread is None or thread.is_alive() == False:
                try:
                    answer = input_timeout.input_with_timeout("", 1)
                except input_timeout.TimeoutExpired:
                    pass
                else:
                    thread = threading.Thread(target=self.create_action_to_send_to_environment, daemon=True)
                    thread.start()
    
    def update_environment_state(self, changed_relations):
        """
        This method is used to update the environment state.
        """
        for item in changed_relations:
            for rel in item:
                if rel[0] == 'new':
                    self.environment_state.add_relation_from_PDDL(rel[1])
                elif rel[0] == 'changed_value':
                    PDDL_relation = self.environment_state.create_relation_from_PDDL(rel[1])
                    environment_state_relation = self.environment_state.find_relation(relation = PDDL_relation, exclude_value = True)
                    environment_state_relation.modify_value(PDDL_relation.value)
                elif rel[0] == 'new_entity':
                    self.environment_state.add_entity_from_PDDL(rel[1])

    def create_action_to_send_to_environment(self):
        """
        This method is used to create the action to send to the environment.
        """
        print("You entered the action builder.")
        i = 0
        for action in self.domain.actions:
            print(str(i) + "- Action: " + action.name)
            i += 1
        print("Write the number of the action you want to create and press enter. To exit press a letter.")
        something = input()
        if something.isdigit():
            i = int(something)
            if i < 0 or i >= len(self.domain.actions):
                print("We accept a range between 0 and "+ str(len(self.domain.actions)-1))
                return
            action = self.domain.actions[i]
            print("Your selected action: ")
            print(action.to_PDDL())
            print("Now choose the parameters of the action.")
            dict_param = {}
            for param in action.parameters:
                print(param)
                print("Choose the entity with type " + param.type.name + ":")
                if action.name.startswith("instantiate_") and param.name == '?obj':
                    entities = ["Apple","GreenKey","RedBook","Bag","GreenPotion","RedCloth","BlueBook","Hammer","RedKey","BlueCloth","Helmet","RedPotion","BlueKey","InkandQuill","Scroll","BluePotion","JewelKey","Skull","Bottle","LitTorch","SpellBook","Bread","Lock","Sword","ChickenLeg","MagnifyingGlass","Coin","OpenScroll","Compass","PurpleBook","Cup","PurpleCloth","EvilBook","PurpleKey","GoldCup","PurplePotion","GreenBook","Rags","Torch"]
                else:
                    entities = self.environment_state.find_entities_with_type(type = param.type.name)
                self.print_entities(entities)
                entity = input("Write the number of the entity and press enter:")
                if entity.isdigit() and int(entity) < len(entities):
                    dict_param[param.name] = entities[int(entity)]
                else:
                    print("You have chosen to exit the action builder.")
                    return
            action_real = Action(action_definition=action, parameters=dict_param)
            result, reason = self.environment_state.can_action_be_applied(action_real, return_reason = True)
            if result:
                message = action_real.get_string_execution()
                print("Action created: " + message)
                print("Sending action to environment...")
                try:
                    result = self.platform_communication.send_message(message)
                except Exception as e:
                    print("Error while sending action to environment: " + str(e))
                finally:
                    print("Action sent to environment.")
            else:
                print("The action cannot be applied because: " + reason)
                print("I'm not sending the action to Camelot. Please try again.")
        else:
            return

    def print_entities(self, entities):
        for j in range(0, len(entities), 2):
            if j+1 < len(entities):
                m = str(j) + ": " + str(entities[j]) +"\t\t\t\t" + str(j+1) + ": " + str(entities[j+1])
            else:
                m = str(j) + ": " + str(entities[j])
            print(m)




if __name__ == '__main__':
    print("Starting Experience Manager...")
    experience_manager = ExperienceManager()
    experience_manager.start_platform_communication()
    experience_manager.main_loop()