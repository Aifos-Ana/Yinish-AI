from macros import *
from boardState import *
from Menu import *
from YinshGame import *
from GUI import *
from IA_player import *


current_file_id = 1


def save_data_to_file(game, difficulty=None, algorithm=None):
    file_name = generate_fileName()
    with open(file_name, "w") as sf:
        
        if(game.is_IA_player):
            sf.write("Game Mode: Human_player as player1 VS IA_player as player2\n")
            sf.write(f"Algorithm used by the IA_player: {'Minimax' if algorithm == MINIMAX_ALGHORITM else 'Negamax' if algorithm == NEGAMAX_ALGHORITM else 'Monte Carlo Tree Search'} in {'hard' if difficulty == 'H' else 'easy' if difficulty == 'E' else 'medium'} level of difficulty\n\n\n")
        else:
            sf.write("\tGame Mode: Human_player as player1 VS Human_Player as player2\n\n\n")

        
        sf.write("Move History:\n")
        
        for move in game.board.move_history:
            sf.write(move + "\n")

        sf.write("\n\n")


        for player, rings in game.scores.items():
            sf.write(f"Rings remove by player{player}: {rings}\n")

        sf.write("\n")
        
        if game.winner == 'Tie':
            sf.write("The game ended in a Tie!")
        else:
            sf.write(f"Player {game.winner} won!")

            sf.write("\n")
            sf.write("\n")

            for player, score in game.calculate_final_scores().items():
                sf.write(f"Player{player}'s score: {score}\n")

      

def generate_fileName():
    global current_file_id
    
    file_name = f"game_{current_file_id}"
    current_file_id += 1
    return file_name


def human_vs_human(menu):
    human_player1 = Human_player()
    human_player2 = Human_player()

    game = YinshGame(human_player1,human_player2)
    gui = GUI(game)
    gui.run()
    menu.show_game_over_menu(game.winner, game.scores,game)
    save_data_to_file(game)

    if menu.clicked_exit:
         pygame.quit()
         exit()


def human_vs_AI(alghoritm, menu): 
        human_player1 = Human_player()
        IA_player2 = IA_player(menu.difficulty, alghoritm) 

        game = YinshGame(human_player1,IA_player2)
        gui = GUI(game)
        gui.run()
        menu.show_game_over_menu(game.winner, game.scores,game)
        save_data_to_file(game, menu.difficulty , alghoritm)

        if menu.clicked_exit:
         pygame.quit()
         exit()



def run():
    menu = Menu()
    menu.show_menu()


    while not menu.clicked_exit:
        
        if menu.human_vs_human:
            human_vs_human(menu)
        elif menu.human_vs_ia:
            human_vs_AI(menu.ai_algorithm,menu) #agora mete o algoritmo de acordo com o menu

run()