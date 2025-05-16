from Menu import *
from macros import *
from boardState import *
from Human_player import * 

class YinshGame:
    def __init__(self, player1, player2):  # Dois underscores antes e depois de "init"
        self.board = boardState()  # Certifica-te que BoardState() está bem importado e existe
        self.current_turn = PLAYER_1  # Player 1 começa
        self.current_round = 0
        self.ring_to_be_moved = {PLAYER_1: (), PLAYER_2:()}
        self.valid_moves = []
        self.track_dir = {(1, 0):[], (-1, 0):[], (0, 1):[], (0, -1):[], (1, -1):[], (-1, 1):[]} #guarda as posições correspondentes a cada direção
        self.scores = {PLAYER_1: 0, PLAYER_2: 0} #guarda os scores de cada jogador
        self.ring_to_remove = None #vê se é necessário o jogador remover o ring depois de ganahr uma linha
        self.game_over = False; #flag para acabar o jogo
        self.reset_game_var = False
        self.winner = None

        
        self.is_IA_player = False
        self.IA_player = None
        self.rings_position_for_IA = []  #talves seja útil para a AI
        self.remove_ring_time = False
        self.choose_ring_time = False
        self.save_time = 0

        if(player2.type == 'IA'):
            player2.board = self.board
            self.is_IA_player = True
            self.IA_player = player2
            self.IA_player.curr_game_state = self
            self.IA_player.curr_board_state = self.board
            print("<--AI player playing!-->")


    
    def place_first_10_rings(self, hex_pos):
        if hex_pos in self.board.hex_positions and self.board.hex_positions[hex_pos] == '0':
            if self.current_turn == PLAYER_1:
                self.board.move_history.append(f"Player 1: Placed Ring at {hex_pos}")

                self.board.hex_positions[hex_pos] = 'R_1' 
                self.current_turn = PLAYER_2
            else:
                self.board.move_history.append(f"Player 2: Placed Ring at {hex_pos}")
                self.board.hex_positions[hex_pos] = 'R_2' 
                self.current_turn = PLAYER_1
            
            self.current_round += 1
            return True
        return False #uma das condições do if sáo inválidas

    def make_move(self, hex_pos=None):
        if self.game_over:
            print("The game is over. No more moves can be made.")
            return False

        # If a ring needs to be removed
        if self.ring_to_remove:
            ##############IA move
            self.remove_ring_time = True
            if self.ring_to_remove == PLAYER_2 and self.is_IA_player:
                self.IA_player.choose_ring()
                self.ring_to_remove = None
                self.current_turn = PLAYER_2 if self.current_turn == PLAYER_1 else PLAYER_1
                return
             ##############IA move
            else:
                if self.board.hex_positions[hex_pos] == f'R_{self.ring_to_remove}':

                    if self.current_turn == PLAYER_1:
                        self.board.move_history.append(f"Player 1: Removed Ring at {hex_pos}")
                    else:
                        self.board.move_history.append(f"Player 2: Removed Ring at {hex_pos}")

                    self.board.hex_positions[hex_pos] = '0'  # Remove the ring
                    print(f"Player {self.ring_to_remove} removed their ring at {hex_pos}")
                    self.ring_to_remove = None  # Reset the flag
                    # Switch turns after removing the ring
                    self.current_turn = PLAYER_2 if self.current_turn == PLAYER_1 else PLAYER_1
                    return True
                else:
                    print(f"Invalid ring removal at {hex_pos}. Player {self.ring_to_remove} must remove one of their own rings.")
                    return False

        # Normal move logic
        print(f"Current ring to be moved for {self.current_turn} turn: {self.ring_to_be_moved[self.current_turn]}")
        


        if self.ring_to_be_moved[self.current_turn]:
            save_val = self.ring_to_be_moved[self.current_turn]
            ##############IA move
            if self.current_turn == PLAYER_2 and self.is_IA_player:
                self.IA_player.move_ring()
                return True
            ##############IA move

            if self.move_ring(hex_pos):  # If the ring is moved, flip markers
                return True

        # First 10 moves to place rings
        if self.current_round < 10:
            ##############IA move
            if self.current_turn == PLAYER_2 and self.is_IA_player:
                self.IA_player.place_10_rings()
            ##############IA move
            else:
                if self.place_first_10_rings(hex_pos):
                    print(f"Placed ring at {hex_pos} for {self.current_turn} turn")
                else:
                    print(f"Failed to place ring at {hex_pos}")
        else:
            ##############IA move
            self.choose_ring_time = True
            if self.current_turn == PLAYER_2 and self.is_IA_player:
                self.IA_player.choose_ring()
                self.choose_ring_time = False
                random_ring_pos = self.ring_to_be_moved[PLAYER_2]
                self.valid_moves = self.get_valid_moves(random_ring_pos)
            ##############IA move
            else:
                if hex_pos in self.board.hex_positions and self.board.hex_positions[hex_pos] == f'R_{self.current_turn}':
                    self.ring_to_be_moved[self.current_turn] = hex_pos

                    if self.current_turn == PLAYER_1:
                        self.board.move_history.append(f"Player 1: Placed Marker at {hex_pos}")
                    else:
                        self.board.move_history.append(f"Player 2: Placed Marker at {hex_pos}")

                    self.valid_moves = self.get_valid_moves(hex_pos)
                    print(f"Valid moves for the selected ring: {self.valid_moves}")
                else:
                    print(f"Failed to place marker at {hex_pos}")

    def move_ring(self, hex_pos):
        if hex_pos not in self.valid_moves:
            print(f"Invalid move! {hex_pos} is not in the valid moves list: {self.valid_moves}")
            return False  # Reject the move

        if self.board.hex_positions[hex_pos] == '0':  # Ensure the position is empty
            previous_pos = self.ring_to_be_moved[self.current_turn]


            if self.current_turn == PLAYER_1:
                self.board.hex_positions[hex_pos] = 'R_1'
                self.board.hex_positions[previous_pos] = 'M_1'
                self.board.move_history.append(f"Player 1: Moved Ring from {previous_pos} to {hex_pos}")

            else:
                self.board.hex_positions[hex_pos] = 'R_2'
                self.board.hex_positions[previous_pos] = 'M_2'

                if self.IA_player:
                    self.board.move_history.append(f"Player 2: Moved Ring from {previous_pos} to {hex_pos}. Time taken: {self.save_time}")
                    self.save_time = None
                else:
                    self.board.move_history.append(f"Player 2: Moved Ring from {previous_pos} to {hex_pos}")



            self.ring_to_be_moved[self.current_turn] = None
            self.valid_moves = []
            self.current_round += 1

            # Flip markers
            used_direction = self.find_used_dir(hex_pos)
            if used_direction is not None:
                self.flip_markers(self.track_dir[used_direction], hex_pos)
            else:
                print(f"Error: No valid direction found for hex_pos {hex_pos}.")

            # Check for 5-marker lines for both players
            for player in [PLAYER_1, PLAYER_2]:
                if self.check_for_five_marker_line(player):     #isto procura
                    print(f"Player {player} scored a point!")
                    self.ring_to_remove = player  # Set the flag to the player who scored
                    return True  # Wait for the player to remove a ring

            # Switch turns if no ring needs to be removed
            self.current_turn = PLAYER_2 if self.current_turn == PLAYER_1 else PLAYER_1
            print(f"Moved ring to {hex_pos}. Now it's {self.current_turn}'s turn.")

            # Reset track_dir after the move is fully processed
            self.track_dir = {(1, 0): [], (-1, 0): [], (0, 1): [], (0, -1): [], (1, -1): [], (-1, 1): []}
            return True

        print(f"Failed to move ring to {hex_pos}")
        return False

    def get_valid_moves(self, ring_pos):
        valid_moves = []
        directions = self.board.get_directions()  # Assuming the board has a method to get movement directions
        found_marker = False

        for direction in directions:
            found_marker = False
            current_pos = ring_pos

            while True:
                next_pos = self.board.get_next_position(current_pos, direction)  # Get the next position in the direction

                if next_pos not in self.board.hex_positions or self.board.hex_positions[next_pos] in ['R_1', 'R_2']:
                    break  # Stop if the position is out of bounds or occupied by a ring

                if self.board.hex_positions[next_pos] in ['M_1', 'M_2']:
                    found_marker = True
                    current_pos = next_pos  # Continue moving past the marker
                    self.track_dir[direction].append(next_pos)
                    continue  # Continue the iteration

                if found_marker and self.board.hex_positions[next_pos] == '0':
                    valid_moves.append(next_pos)  # Add only empty spaces as valid moves
                    current_pos = next_pos  # Move forward
                    self.track_dir[direction].append(next_pos)
                    break  # Stop after finding a valid move

                self.track_dir[direction].append(next_pos)
                valid_moves.append(next_pos)  # Add only empty spaces as valid moves
                current_pos = next_pos  # Move forward

        return valid_moves
    
    
    def find_used_dir(self, end_position):  
        print(f"Finding direction for position: {end_position}")
        print(f"Current track_dir: {self.track_dir}")
        for direction, positions in self.track_dir.items():
            for position in positions:
                if position == end_position:
                    return direction
        print(f"Error: Direction for position {end_position} not found in track_dir.")
        return None

    def flip_markers(self, positions, end_pos):
        #para agora dá flip a tudo
        for position in positions:
            if position == end_pos:
                return # esta condição dá bem porque as posições esstão por ordem, quando chega a end_pos para de virar os markers que estão naquela linha
            
            if self.board.hex_positions[position] == 'M_1':
                self.board.hex_positions[position] = 'M_2'
            elif self.board.hex_positions[position] == 'M_2':
                self.board.hex_positions[position] = 'M_1'  
    
    def get_board(self):
        return self.board

    def check_for_five_marker_line(self, player):
        directions = self.board.get_directions()  # Get all possible directions
        player_marker = f'M_{player}'  # Marker type for the specified player

        for position, marker in self.board.hex_positions.items():
            if marker != player_marker:
                continue  # Skip positions that don't belong to the player's markers

            for direction in directions:
                line = [position]  # Start with the current position
                current_pos = position

                # Check forward in the direction
                while True:
                    next_pos = self.board.get_next_position(current_pos, direction)
                    if next_pos in self.board.hex_positions and self.board.hex_positions[next_pos] == player_marker:
                        line.append(next_pos)
                        current_pos = next_pos
                    else:
                        break

                # If a line of 5 markers is found
                if len(line) >= 5:
                    self.scores[player] += 1  # Increment the specified player's score
                    print(f"Player {player} scores 1 point! Current score: {self.scores[player]}")

                    if len(line) % 5:
                        self.remove_markers(line)  # Remove the markers in the line
                    else:
                        self.remove_markers(line[:5])


                    self.ring_to_remove = player  # Set the flag to remove a ring

                    # Check if the player has won the game
                    if self.scores[player] == 3:
                        print(f"Player {player} wins the game!")
                        self.game_over = True  # Set the game over flag

                        # Calculate and print final scores for debugging
                        final_scores = self.calculate_final_scores()
                        print(f"Final Scores: Player 1: {final_scores[PLAYER_1]:.3f}, Player 2: {final_scores[PLAYER_2]:.3f}")
                        self.game_over = True
                        self.reset_game_var = True
                        self.winner = player

                    return True  

        # Check for a tie if no 5-marker line is found
        if self.check_for_tie():
            self.game_over = True
            self.reset_game_var = True
            self.winner = "Tie"
            return True

        return False  # No line found

    def remove_markers(self, positions):
        for pos in positions:
            self.board.hex_positions[pos] = '0'  # Reset the position to empty
        print(f"Removed markers at positions: {positions}")


    def get_ring_margin_score(self, rings_removed, opponent_rings_removed):

        return RING_MARGIN_LOOKUP.get((rings_removed, opponent_rings_removed), 0)

    def calculate_final_scores(self):
        """Calculates the final scores for both players."""
        final_scores = {}

        for player in [PLAYER_1, PLAYER_2]:
            opponent = PLAYER_2 if player == PLAYER_1 else PLAYER_1
            
            # Calculate Ring Margin Score using lookup table
            rings_removed = self.scores[player]
            opponent_rings_removed = self.scores[opponent]
            ring_margin_score = self.get_ring_margin_score(rings_removed, opponent_rings_removed)

            # Calculate Marker Margin Score
            markers_remaining = sum(1 for pos, marker in self.board.hex_positions.items() if marker == f'M_{player}')
            marker_margin_score = markers_remaining / 1000

            # Final Score
            final_scores[player] = ring_margin_score + marker_margin_score

        return final_scores

    def check_for_tie(self):
        """Checks if the game ends in a tie (all 51 markers placed)."""
        total_markers = sum(1 for pos, marker in self.board.hex_positions.items() if marker in ['M_1', 'M_2'])
        if total_markers == MARKER_AVAIL and self.scores[PLAYER_1] < 3 and self.scores[PLAYER_2] < 3:
            print("The game ends in a tie! All 51 markers have been placed.")
            self.game_over = True
            return True
        return False