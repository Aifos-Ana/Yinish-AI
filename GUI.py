from macros import *
import time

class GUI:
    def __init__(self, game):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Yinsh Board")
        self.board = game.get_board()
        self.game = game 
        self.font = pygame.font.Font(None, 50)
        self.pixel_positions = {
            (q, r): self.hex_to_pixel(q, r) for q, r, _ in self.board.hex_positions
        }

    def hex_to_pixel(self, q, r):
        """Convert hexagonal grid coordinates (q, r) to screen pixel coordinates."""
        x = CENTER_X + HEX_RADIUS * (3 / 2 * q)
        y = CENTER_Y + HEX_RADIUS * (math.sqrt(3) * (r + q / 2))
        return x, y

    def pixel_to_hex(self, x, y):
        """Convert pixel coordinates to the closest hex grid coordinates."""
        min_dist = float('inf')
        closest_hex = None

        for (q, r), (hx, hy) in self.pixel_positions.items():
            dist = math.sqrt((hx - x) ** 2 + (hy - y) ** 2)
            if dist < min_dist:
                min_dist = dist
                s = -q -r
                closest_hex = (q, r , s)

        return closest_hex if min_dist < HEX_RADIUS else None  # Click must be within range

    def draw_hex_grid(self):
        """Draw a hexagonal grid with connecting lines and circles."""
        self.screen.fill(BG_COLOR)

        # Draw connecting lines
        for (q, r), (x, y) in self.pixel_positions.items():
            neighbors = [
                (q + 1, r), (q - 1, r),  # Left and right
                (q, r + 1), (q, r - 1),  # Up-right, Down-left
                (q + 1, r - 1), (q - 1, r + 1)  # Down-right, Up-left
            ]

            for nq, nr in neighbors:
                if (nq, nr) in self.pixel_positions:
                    nx, ny = self.pixel_positions[(nq, nr)]
                    pygame.draw.line(self.screen, BLACK, (x, y), (nx, ny), 2)

            
        pos_selected_ring_p1 = self.game.ring_to_be_moved[PLAYER_1] #isto não está registado no board, no board só são markers e rings, n á sobrepostos, para agora tá a resultar
        pos_selected_ring_p2 = self.game.ring_to_be_moved[PLAYER_2]

        # Draw placed stones
        for (q, r , s), symbol in self.board.hex_positions.items():
            x, y = self.hex_to_pixel(q,r)

            if pos_selected_ring_p1 and pos_selected_ring_p1 == (q,r,s): #posião do ring a ser movido, pintar como ring sobreposto de um marker. No board a posição é M_1
                self.draw_circle(x, y, color=WHITE)  
                pygame.draw.circle(self.screen, "blue", (x, y), 26, 6)  
            elif pos_selected_ring_p2 and pos_selected_ring_p2 == (q,r,s):
                self.draw_circle(x, y, color=BLACK)  
                pygame.draw.circle(self.screen, "red", (x, y), 26, 6)  
            else:
                match symbol:
                    case '0':
                        pass
                    case 'R_1':
                        if self.game.ring_to_remove and self.game.ring_to_remove == PLAYER_1:
                            self.draw_ring(x, y, BRIGHT_BLUE, glow=True)
                        else:
                            self.draw_ring(x, y, "blue")
                    case 'R_2':
                        if self.game.ring_to_remove and self.game.ring_to_remove == PLAYER_2:
                            self.draw_ring(x, y, BRIGHT_RED, glow=True)
                        else:
                            self.draw_ring(x, y, "red")
                    case 'M_1':
                        self.draw_circle(x, y, "white")
                    case 'M_2':
                        self.draw_circle(x, y, "black")

            
            if (q,r,s) in self.game.valid_moves: 
                pygame.draw.circle(self.screen, "grey", (x, y), 20, 4)  



        self.draw_player_turn()

        # Draw win rings
        self.draw_win_rings()

        pygame.display.update()
        
            
    def draw_player_turn(self):
    
        turn_text = f"Player turn: {'1' if self.game.current_turn == PLAYER_1 else '2'}"
        text_surface = self.font.render(turn_text, True, "blue" if self.game.current_turn == PLAYER_1 else "red")
    
        self.screen.blit(text_surface, (20, 20))  

    def draw_circle(self, x, y, color):
        """Draw a smaller stone at the given position."""
        pygame.draw.circle(self.screen, BLACK, (x, y), CIRCLE_RADIUS - 9 + 2)  
        pygame.draw.circle(self.screen, color, (x, y), CIRCLE_RADIUS - 9)  

    def draw_ring(self, x, y, color, glow=False):
        """Draw a larger ring at the given position, with optional glow."""
    
        if glow:
            glow_color = (255, 255, 255, 100)  # Branco semi-transparente
            glow_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, (30, 30), 30)
            self.screen.blit(glow_surface, (x - 30, y - 30))
    
        pygame.draw.circle(self.screen, color, (x, y), 26, 6)    

    def draw_win_rings(self):
        """Draw GUI rings (top-right & bottom-left corners) based on player scores."""
        player_colors = {PLAYER_1: "blue", PLAYER_2: "red"}  # Define player colors
        total_rings = len(GUI_RING_POSITIONS)  # Total number of rings to display
        player_1_rings = self.game.scores[PLAYER_1]
        player_2_rings = self.game.scores[PLAYER_2]

        # Draw rings for Player 1
        for i in range(player_1_rings):
            x, y = GUI_RING_POSITIONS[i]
            self.draw_ring(x, y, player_colors[PLAYER_1])

        # Draw rings for Player 2
        for i in range(player_2_rings):
            x, y = GUI_RING_POSITIONS[total_rings - 1 - i]
            self.draw_ring(x, y, player_colors[PLAYER_2])

        # Draw remaining idle rings
        for i in range(player_1_rings, total_rings - player_2_rings):
            x, y = GUI_RING_POSITIONS[i]
            self.draw_ring(x, y, IDLE_RING_COLOR)

    def handle_click(self, x, y):
        """Handles a click event to place a stone if valid."""
        clicked_hex = self.pixel_to_hex(x, y)

        if clicked_hex:
            self.game.make_move(clicked_hex)

    def run(self):
        """Run the game loop: menu, board, and interactions."""

        running = True
        while running:
            if self.game.reset_game_var:
                return
            
            self.draw_hex_grid()

            if (self.game.is_IA_player and self.game.current_turn == PLAYER_2) or self.game.ring_to_remove == PLAYER_2 and self.game.is_IA_player:
                self.game.make_move()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        self.handle_click(x, y)

        pygame.quit()