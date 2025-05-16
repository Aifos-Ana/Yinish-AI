from macros import *
import math
import random
import copy # create a deep copy of an object, meaning that it recursively copies all objects within the original object, creating entirely new instances of them. This ensures that changes made to the copied object do not affect the original object and vice versa.
import time

class MCTSNode:
    def __init__(self, game_state, parent=None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.move = None  # (from_pos, to_pos)
        self.untried_moves = []  # Lista de movimentos não tentados

        for pos, piece in self.game_state.board.hex_positions.items():
            if piece == "R_2":
                valid_moves = self.game_state.get_valid_moves(pos)
                self.untried_moves.extend([(pos, move) for move in valid_moves])

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, exploration_weight=1.4):
        """ Uses UCB1 formula to select the best child node """
        if not self.children:
            return None
        
        def ucb1(node):
            return (node.wins / (node.visits + 1e-6)) + exploration_weight * math.sqrt(math.log(self.visits + 1) / (node.visits + 1e-6))

        return max(self.children, key=ucb1)

    def expand(self, max_expansions=10):
        if self.untried_moves:
            num_expansions = min(max_expansions, len(self.untried_moves))
            moves_to_expand = random.sample(self.untried_moves, num_expansions)
            for (from_pos, to_pos) in moves_to_expand:
                # ... (o resto do teu código de expand)
                new_state = copy.deepcopy(self.game_state)
                new_state.board.hex_positions[from_pos] = 'M_2'
                new_state.board.hex_positions[to_pos] = 'R_2'
                new_state.ring_to_be_moved[PLAYER_2] = to_pos
                new_state.check_for_five_marker_line(PLAYER_2)

                child_node = MCTSNode(new_state, parent=self)
                child_node.move = (from_pos, to_pos)
                self.children.append(child_node)
                self.untried_moves.remove((from_pos, to_pos)) # Remover o movimento já expandido
                return child_node # Podemos retornar o primeiro filho expandido para continuar a exploração
        return None

    def update(self, result):
        """ Backpropagates the result of a simulation """
        self.visits += 1
        self.wins += result


class IA_player:
    def __init__(self, difficulty, algorithm):
        self.depth = 6 if difficulty == 'H' else (3 if difficulty == 'E' else 4)  # Depth for Minimax
        self.type = 'IA'
        self.algorithm = algorithm  # Algorithm type: MINIMAX_ALGHORITM or MONTE_CARLO_ALGHORITM
        self.board = None
        self.curr_game_state = None
        self.curr_board_state = None
        self.best_ring_pos = None
        print(f"IA PLAYER CALLED WITH DIFFICULTY {difficulty} AND ALGHORITM {algorithm}")

    def place_10_rings(self):
        valid_positions = self.get_valid_moves(self.curr_game_state, '0')
        if valid_positions:
            random_pos = random.choice(valid_positions)
            print(f"AI escolheu a posição {random_pos} para colocar um anel.")
            self.curr_game_state.place_first_10_rings(random_pos)


    def choose_ring(self):
        start = time.time()

        valid_positions = self.get_valid_moves(self.curr_game_state, 'R_2')
        alpha = float('-inf')
        beta = float('inf')

        if self.curr_game_state.choose_ring_time and self.curr_game_state.current_turn == PLAYER_2:
            if valid_positions:
                if self.algorithm == MINIMAX_ALGHORITM:
                    best_score = float('-inf')
                    best_pos = None

                    for pos in valid_positions:
                        simulated_board = copy.deepcopy(self.curr_game_state)
                        simulated_board.ring_to_be_moved[PLAYER_2] = pos
                        score = self.minimax(simulated_board, self.depth, False, alpha, beta)

                        if score > best_score:
                            best_score = score
                            best_pos = pos

                    self.best_ring_pos = best_pos
                    self.curr_game_state.ring_to_be_moved[PLAYER_2] = best_pos
                    self.curr_game_state.choose_ring_time = False

                    end = time.time()
                    self.curr_game_state.board.move_history.append(f"Player 2: Placed Marker at {best_pos}. Time taken: {end - start:.4f}s")
                elif self.algorithm == MONTE_CARLO_ALGHORITM:
                    best_pos = self.monte_carlo_tree_search_choose_ring()
                    self.curr_game_state.ring_to_be_moved[PLAYER_2] = best_pos
                    self.curr_game_state.choose_ring_time = False
                    end = time.time()
                    self.curr_game_state.board.move_history.append(f"Player 2: Placed Marker at {best_pos}. Time taken: {end - start:.4f}s")

        else:
            if self.curr_game_state.remove_ring_time:
                if valid_positions:
                    random_pos = random.choice(valid_positions)
                    self.curr_game_state.board.hex_positions[random_pos] = '0'  # Remove the ring
                    self.curr_game_state.board.move_history.append(f"Player 2: Removed Ring at {random_pos}")
                self.curr_game_state.remove_ring_time = False

    def move_ring(self):
        start = time.time()
        ring_to_move = self.curr_game_state.ring_to_be_moved[PLAYER_2]

        if self.algorithm == MINIMAX_ALGHORITM:
            best_move = self.minimax_decision()
        elif self.algorithm == MONTE_CARLO_ALGHORITM:
            best_move = self.monte_carlo_tree_search_move_ring()

        valid_moves = self.curr_game_state.get_valid_moves(ring_to_move)

        if best_move:
            moved_successfully = self.curr_game_state.move_ring(best_move)
            end = time.time()
            self.curr_game_state.save_time = f'{end - start:.4f}s'
            
    def minimax_decision(self):
        valid_moves = self.curr_game_state.get_valid_moves(self.curr_game_state.ring_to_be_moved[PLAYER_2])
        best_score = float('-inf')
        best_move = None

        alpha = float('-inf')
        beta = float('inf')

        for move in valid_moves:
            simulated_board = copy.deepcopy(self.curr_game_state)
            simulated_board.move_ring(move)
            score = self.minimax(simulated_board, self.depth - 1, False, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, game, depth, is_maximizing,alpha,beta):
        if depth == 0 or game.game_over or game.reset_game_var:
            return self.evaluate_board_state(game)

        if is_maximizing:
            max_eval = float('-inf')
            possible_moves = self.get_valid_moves(game, 'R_2')
            for move in possible_moves:
                simulated_board = copy.deepcopy(game, memo={})
                simulated_board.ring_to_be_moved[PLAYER_2] = move
                evaluation = self.minimax(simulated_board, depth - 1, False,alpha,beta)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha,evaluation)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            possible_moves = self.get_valid_moves(game, 'R_1')
            for move in possible_moves:
                simulated_board = copy.deepcopy(game, memo={})
                simulated_board.ring_to_be_moved[PLAYER_1] = move
                evaluation = self.minimax(simulated_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, evaluation)
                beta = min(beta,evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board_state(self, game):
    
        final_scores = {}

        for player in [PLAYER_1, PLAYER_2]:
            opponent = PLAYER_2 if player == PLAYER_1 else PLAYER_1

            rings_removed = game.scores[player]
            opponent_rings_removed = game.scores[opponent]
            ring_margin_score = game.get_ring_margin_score(rings_removed, opponent_rings_removed)

            
            markers_remaining = sum(1 for pos, marker in game.board.hex_positions.items() if marker == f'M_{player}')
            marker_margin_score = markers_remaining

            blocking_score = self.detect_blocking_opportunity(player, game)

            final_scores[player] = ring_margin_score + marker_margin_score + 0.2 * blocking_score

        return final_scores[PLAYER_2] - final_scores[PLAYER_1]  

    def detect_blocking_opportunity(self, player, game):
        directions = game.board.get_directions()  
        opponent = PLAYER_2 if player == PLAYER_1 else PLAYER_1
        opponent_marker = f'M_{opponent}'
        blocking_score = 0  

        for position, marker in game.board.hex_positions.items():
            if marker != opponent_marker:
                continue  

            for direction in directions:
                current_pos = position
                line = [position]  
                empty_spots = []  
                marker_count = 1  
                
                while True:
                    next_pos = game.board.get_next_position(current_pos, direction)

                    if next_pos is None or next_pos not in game.board.hex_positions:
                        break

                    next_marker = game.board.hex_positions[next_pos]

                    if next_marker == opponent_marker:
                        marker_count += 1
                        line.append(next_pos)
                        current_pos = next_pos 
                    elif next_marker == '0':  
                        empty_spots.append(next_pos)
                        break  
                    else:
                        break 

                if marker_count == 3 and len(empty_spots) == 1:
                    blocking_score += 5 

                elif marker_count == 2 and len(empty_spots) == 2:
                    blocking_score += 2  

        return blocking_score 

    def get_valid_moves(self, curr_board_state, condition):
        return [pos for pos, val in curr_board_state.board.hex_positions.items() if val == condition]
    
    def monte_carlo_tree_search_choose_ring(self):
        """ Uses MCTS to decide the best ring to choose. """
        root = MCTSNode(copy.deepcopy(self.curr_game_state))

        time_limit = time.time() + 2 # Run MCTS for 2 seconds
        while time.time() < time_limit:
            node = self.select(root)
            if not node.is_fully_expanded():
                node = node.expand()
            result = self.simulate(node.game_state)
            self.backpropagate(node, result)

        best_node = root.best_child(exploration_weight=0)
        return best_node.game_state.ring_to_be_moved[PLAYER_2] if best_node else random.choice(root.untried_moves)

    def monte_carlo_tree_search_move_ring(self):
        print("MCTS move_ring started") # Added print
        """ Uses MCTS to decide the best move for the ring. """
        root = MCTSNode(copy.deepcopy(self.curr_game_state))

        time_limit = time.time() + 2 # Run for 2 seconds
        while time.time() < time_limit:
            node = self.select(root)
            if not node.is_fully_expanded():
                node = node.expand()
            result = self.simulate(node.game_state)
            self.backpropagate(node, result)

        best_node = root.best_child(exploration_weight=0)
        print("MCTS move_ring finished") # Added print
        return best_node.move[1] if best_node and best_node.move else None
    
    def select(self, node):
        """ Selection phase: Select the best child node using UCB1 """
        while node.is_fully_expanded() and node.children:
            node = node.best_child()
        return node

    def simulate(self, game_state, max_moves=500):
        simulated_state = copy.deepcopy(game_state)
        move_count = 0
        current_player = PLAYER_2

        while not simulated_state.game_over and move_count < max_moves:
            move_count += 1
            ring_positions = [pos for pos, val in simulated_state.board.hex_positions.items() if val == f'R_{current_player}']
            if not ring_positions:
                break
            from_pos = random.choice(ring_positions)
            valid_moves = simulated_state.get_valid_moves(from_pos)
            if not valid_moves:
                current_player = PLAYER_1 if current_player == PLAYER_2 else PLAYER_2
                continue

            # Em vez de escolher um movimento aleatório, podemos avaliar os próximos estados
            best_move = None
            best_score = float('-inf') if current_player == PLAYER_2 else float('inf')

            for to_pos in valid_moves:
                temp_state = copy.deepcopy(simulated_state)
                temp_state.board.hex_positions[from_pos] = f'M_{current_player}'
                temp_state.board.hex_positions[to_pos] = f'R_{current_player}'
                temp_state.ring_to_be_moved[current_player] = to_pos
                score = self.evaluate_board_state(temp_state) # Usando a heurística do Minimax

                if current_player == PLAYER_2:
                    if score > best_score:
                        best_score = score
                        best_move = to_pos
                else:
                    if score < best_score:
                        best_score = score
                        best_move = to_pos

            if best_move:
                simulated_state.board.hex_positions[from_pos] = f'M_{current_player}'
                simulated_state.board.hex_positions[best_move] = f'R_{current_player}'
                simulated_state.ring_to_be_moved[current_player] = best_move
            else:
                to_pos = random.choice(valid_moves) # Se não houver um "melhor" movimento, escolhe um aleatório
                simulated_state.board.hex_positions[from_pos] = f'M_{current_player}'
                simulated_state.board.hex_positions[to_pos] = f'R_{current_player}'
                simulated_state.ring_to_be_moved[current_player] = to_pos

            current_player = PLAYER_1 if current_player == PLAYER_2 else PLAYER_2

        return 1 if simulated_state.scores[PLAYER_2] > simulated_state.scores[PLAYER_1] else 0
    
    def backpropagate(self, node, result):
        """ Backpropagation phase: Update the win/loss results up the tree """
        while node is not None:
            node.update(result)
            node = node.parent