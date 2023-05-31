from singleton_decorator import singleton

@singleton
class PlayerModel:

    def __init__(self):
        self.fighter = 0
        self.method_actor = 0 
        self.storyteller = 0
        self.tactician = 0 
        self.power_gamer = 0
    
    def update_player_model(self, fighter = 0, method_actor = 0, storyteller = 0, tactician = 0, power_gamer = 0):
        """
        Method used to update the player model.

        Parameters
        ----------
        fighter : int
            The fighter value to add to the player model.
        method_actor : int
            The method actor value to add to the player model.
        storyteller : int
            The storyteller value to add to the player model.
        tactician : int
            The tactician value to add to the player model.
        power_gamer : int
            The power gamer value to add to the player model.
        """
        self.fighter += fighter
        self.method_actor += method_actor
        self.storyteller += storyteller
        self.tactician += tactician
        self.power_gamer += power_gamer
    
    def update_player_model_from_message(self, message : str):
        """
        Method used to update the player model from a message.

        Parameters
        ----------
        message : str
            The message to update the player model from.
        """
        message = message[1:-1]
        fighter, method_actor, storyteller, tactician, power_gamer = message.replace("'", '').split(",")
        self.update_player_model(int(fighter), int(method_actor), int(storyteller), int(tactician), int(power_gamer))
        self.print_player_model()

    def get_top_two_player_model_types(self):
        """
        Method used to get the top two player model types.

        Returns
        -------
        list
            A list of the top two player model types.
        """
        player_model_types = ["fighter", "method_actor", "storyteller", "tactician", "power_gamer"]
        player_model_values = [self.fighter, self.method_actor, self.storyteller, self.tactician, self.power_gamer]
        top_two_player_model_types = []
        for i in range(2):
            max_value = max(player_model_values)
            max_value_index = player_model_values.index(max_value)
            top_two_player_model_types.append(player_model_types[max_value_index])
            player_model_values[max_value_index] = -1
        return top_two_player_model_types
    
    def print_player_model(self):
        return_string = "Player model: "
        return_string += "Fighter: " + str(self.fighter) + ", "
        return_string += "Method actor: " + str(self.method_actor) + ", "
        return_string += "Storyteller: " + str(self.storyteller) + ", "
        return_string += "Tactician: " + str(self.tactician) + ", "
        return_string += "Power gamer: " + str(self.power_gamer)
        print(return_string)