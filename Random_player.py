from macros import *
import random

class Random_player:
    def __init__(self):
        self.type = 'IA'
        self.board = []
        self.curr_game_state = None
        self.curr_board_state = None



    def place_10_rings(self):
            # Escolher apenas posições vazias
            valid_positions = [pos for pos, val in self.curr_board_state.hex_positions.items() if val == '0']
            
            if valid_positions:  # Verifica se há posições disponíveis
                random_pos = random.choice(valid_positions)
                print(f"AI escolheu a posição {random_pos} para colocar um anel.")
                
                self.curr_game_state.place_first_10_rings(random_pos)  
            


    def choose_ring(self):
        valid_positions = [pos for pos, val in self.curr_board_state.hex_positions.items() if val == 'R_2']

        if self.curr_game_state.choose_ring_time and self.curr_game_state.current_turn == PLAYER_2:
            if valid_positions:
                random_pos = random.choice(valid_positions)
                self.curr_game_state.ring_to_be_moved[PLAYER_2] = random_pos
            self.curr_game_state.choose_ring_time = False
            
        else:
            if self.curr_game_state.remove_ring_time:
                if valid_positions:
                    random_pos = random.choice(valid_positions)
                    self.curr_game_state.board.hex_positions[random_pos] = '0'  # Remove the ring

                self.curr_game_state.remove_ring_time = False
            else:
                return
        




    def move_ring(self):
        valid_positions = self.curr_game_state.valid_moves

        if valid_positions:
            random_pos = random.choice(valid_positions)

            self.curr_game_state.move_ring(random_pos)
