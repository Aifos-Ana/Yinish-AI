from macros import *
import math

class boardState:
    def __init__(self, previous_boardState=None, moveHistory=None):
        self.move_history = moveHistory if moveHistory is not None else []
        self.hex_positions = previous_boardState.copy() if previous_boardState is not None else self.generate_hex_positions()

    def generate_hex_positions(self):
        """Generate hexagonal grid positions using cube coordinates, removing vertices."""
        hex_positions = {}
        vertices = {
            (BOARD_SIZE, 0, -BOARD_SIZE),
            (-BOARD_SIZE, 0, BOARD_SIZE),
            (0, BOARD_SIZE, -BOARD_SIZE),
            (0, -BOARD_SIZE, BOARD_SIZE),
            (BOARD_SIZE, -BOARD_SIZE, 0),
            (-BOARD_SIZE, BOARD_SIZE, 0),
        }

        for q in range(-BOARD_SIZE, BOARD_SIZE + 1):
            for r in range(-BOARD_SIZE, BOARD_SIZE + 1):
                s = -q - r
                if -BOARD_SIZE <= s <= BOARD_SIZE and (q, r, s) not in vertices:
                    hex_positions[(q, r, s)] = "0"  # Estado inicial

        return hex_positions

    def get_directions(self):
        """
        Return all possible movement directions on the hexagonal board.
        :return: A list of direction vectors (e.g., [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]).
        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        return directions

    def get_next_position(self, current_pos, direction):
        if isinstance(current_pos, str):  # Check if it's a string
            print(f"Error: current_pos is a string instead of a tuple! Value: {current_pos}")
            return None  # Or handle it in a way that prevents the error

        return (
            current_pos[0] + direction[0],
            current_pos[1] + direction[1],
            current_pos[2] - direction[0] - direction[1]
        )


    def hex_to_screen(self, hex_pos):
        """
        Convert hexagonal grid coordinates (q, r, s) to screen pixel coordinates.
        :param hex_pos: A tuple (q, r, s) representing hex coordinates.
        :return: A tuple (x, y) representing screen coordinates.
        """
        q, r, s = hex_pos
        x = CENTER_X + HEX_RADIUS * (3 / 2 * q)
        y = CENTER_Y + HEX_RADIUS * (math.sqrt(3) * (r + q / 2))
        return int(x), int(y)

