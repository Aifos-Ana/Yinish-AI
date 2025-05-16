from GUI import *
from macros import *

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Menu")
        self.font = pygame.font.Font(None, 50)  # Initialized after pygame.init()
        img = pygame.image.load('icon.gif')
        pygame.display.set_icon(img)
        self.human_vs_human = False
        self.human_vs_ia = False
        self.ai_algorithm = None  # Store selected AI algorithm
        self.difficulty = None  # Store selected difficulty
        self.clicked_exit = False

    def show_menu(self):
        """Exibe o menu principal."""
        menu_running = True
        while menu_running:
            self.screen.fill((50, 50, 50))
            start_rect = pygame.Rect(300, 200, 200, 60)
            exit_rect = pygame.Rect(300, 300, 200, 60)

            start_text = self.font.render("Start Game", True, WHITE)
            exit_text = self.font.render("Exit", True, WHITE)

            self.screen.blit(start_text, (320, 210))
            self.screen.blit(exit_text, (370, 310))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if start_rect.collidepoint(x, y):
                        self.show_submenu()  # Show the submenu
                        return
                    elif exit_rect.collidepoint(x, y):
                        pygame.quit()
                        exit()

    def show_submenu(self):
        """Exibe o submenu para escolher o modo de jogo."""
        submenu_running = True
        while submenu_running:
            self.screen.fill((50, 50, 50))
            two_players_rect = pygame.Rect(300, 200, 200, 60)
            player_vs_ia_rect = pygame.Rect(300, 300, 200, 60)
            back_rect = pygame.Rect(300, 400, 200, 60)

            two_players_text = self.font.render("2 Players", True, WHITE)
            player_vs_ia_text = self.font.render("Player vs AI", True, WHITE)
            back_text = self.font.render("Back", True, WHITE)

            self.screen.blit(two_players_text, (320, 210))
            self.screen.blit(player_vs_ia_text, (310, 310))
            self.screen.blit(back_text, (370, 410))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if two_players_rect.collidepoint(x, y):
                        self.human_vs_human = True
                        submenu_running = False  # Exit the submenu loop
                    elif player_vs_ia_rect.collidepoint(x, y):
                        self.human_vs_ia = True
                        self.show_ai_algorithm_menu()  # Show AI algorithm menu
                        submenu_running = False  # Exit the submenu loop
                    elif back_rect.collidepoint(x, y):
                        submenu_running = False  # Exit the submenu loop to return to the main menu
                        self.show_menu()

    def show_ai_algorithm_menu(self):
        """Exibe o menu para escolher o algoritmo de IA."""
        algorithm_running = True
        while algorithm_running:
            self.screen.fill((50, 50, 50))
            minimax_rect = pygame.Rect(300, 200, 200, 60)
            mcts_rect = pygame.Rect(300, 300, 200, 60)
            back_rect = pygame.Rect(300, 400, 200, 60)

            minimax_text = self.font.render("Minimax", True, WHITE)
            mcts_text = self.font.render("MCTS", True, WHITE)
            back_text = self.font.render("Back", True, WHITE)

            self.screen.blit(minimax_text, (350, 210))
            self.screen.blit(mcts_text, (370, 310))
            self.screen.blit(back_text, (370, 410))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if minimax_rect.collidepoint(x, y):
                        self.ai_algorithm = MINIMAX_ALGHORITM
                        self.show_difficulty_menu()  # Show difficulty menu
                        algorithm_running = False  # Exit the algorithm menu loop
                    elif mcts_rect.collidepoint(x, y):
                        self.ai_algorithm = MONTE_CARLO_ALGHORITM
                        self.show_difficulty_menu()  # Show difficulty menu
                        algorithm_running = False  # Exit the algorithm menu loop
                    elif back_rect.collidepoint(x, y):
                        algorithm_running = False  # Exit the algorithm menu loop to return to the submenu
                        self.show_submenu()

    def show_difficulty_menu(self):
        """Exibe o menu para escolher a dificuldade."""
        difficulty_running = True
        while difficulty_running:
            self.screen.fill((50, 50, 50))
            easy_rect = pygame.Rect(300, 150, 200, 60)
            normal_rect = pygame.Rect(300, 250, 200, 60)
            hard_rect = pygame.Rect(300, 350, 200, 60)
            back_rect = pygame.Rect(300, 450, 200, 60)

            easy_text = self.font.render("Easy", True, WHITE)
            normal_text = self.font.render("Medium", True, WHITE)
            hard_text = self.font.render("Hard", True, WHITE)
            back_text = self.font.render("Back", True, WHITE)

            self.screen.blit(easy_text, (350, 160))
            self.screen.blit(normal_text, (340, 260))
            self.screen.blit(hard_text, (350, 360))
            self.screen.blit(back_text, (350, 460))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if easy_rect.collidepoint(x, y):
                        self.difficulty = 'E'
                        difficulty_running = False  # Exit the difficulty menu loop
                    elif normal_rect.collidepoint(x, y):
                        self.difficulty = 'M'
                        difficulty_running = False  # Exit the difficulty menu loop
                    elif hard_rect.collidepoint(x, y):
                        self.difficulty = 'H'
                        difficulty_running = False  # Exit the difficulty menu loop
                    elif back_rect.collidepoint(x, y):
                        difficulty_running = False  # Exit the difficulty menu loop to return to the algorithm menu
                        self.show_ai_algorithm_menu()

    def start_two_players_game(self):
        """Inicia o jogo no modo 2 jogadores."""
        game_running = True
        while game_running:
            return
          

    def show_game_over_menu(self, winner, scores, game):
        """Displays the game over menu with the winner, statistics, and final scores."""
        final_scores = game.calculate_final_scores()  # Calculate final scores
        game_over_running = True
        self.clicked_exit = False
        while game_over_running:
            self.screen.fill((50, 50, 50))

            # Display the winner or tie
            if winner == "Tie":
                winner_text = self.font.render("The game ends in a Tie!", True, WHITE)
            else:
                winner_text = self.font.render(f"Player {winner} Wins!", True, WHITE)
            self.screen.blit(winner_text, (300, 150))

            # Display the scores
            player_1_score_text = self.font.render(f"Player 1 Score: {scores[PLAYER_1]}", True, WHITE)
            player_2_score_text = self.font.render(f"Player 2 Score: {scores[PLAYER_2]}", True, WHITE)
            self.screen.blit(player_1_score_text, (300, 250))
            self.screen.blit(player_2_score_text, (300, 300))

            # Display the final scores
            player_1_final_score_text = self.font.render(f"Player 1 Final Score: {final_scores[PLAYER_1]:.3f}", True, WHITE)
            player_2_final_score_text = self.font.render(f"Player 2 Final Score: {final_scores[PLAYER_2]:.3f}", True, WHITE)
            self.screen.blit(player_1_final_score_text, (300, 350))
            self.screen.blit(player_2_final_score_text, (300, 400))

            # Display the "Play Again" and "Exit" buttons
            play_again_rect = pygame.Rect(300, 500, 200, 60)
            exit_rect = pygame.Rect(300, 600, 200, 60)
            play_again_text = self.font.render("Play Again", True, WHITE)
            exit_text = self.font.render("Exit", True, WHITE)
            self.screen.blit(play_again_text, (320, 510))
            self.screen.blit(exit_text, (370, 610))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over_running = False
                    self.clicked_exit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if play_again_rect.collidepoint(x, y):
                        game.reset_game_var = True  # Reset the game state
                        game_over_running = False  # Exit the game over menu
                    elif exit_rect.collidepoint(x, y):
                        game_over_running = False
                        self.clicked_exit = True


