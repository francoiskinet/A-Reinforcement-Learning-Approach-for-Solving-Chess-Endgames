from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt
from Play import Play
from Pieces import Rook, Queen
from BaseParams import DIRECTORY_PATH




def export_dict(dictionnaire, nom_de_fichier, mode = 'a'):
    with open(nom_de_fichier, mode) as fichier:
        for cle, valeur in dictionnaire.items():
            fichier.write(f'{cle}: {valeur}\n')



def calc_winrate(args):
    result_dict = {}
    base_memory, games_to_play, learning_rate, eps, piece, gamma, epoch, parameter = args
    filename = base_memory + piece.__name__ + '_Q_trained_ep' + str(epoch) + '_g' + str(int(gamma * 100)) + \
                        '_l' + str(int(learning_rate * 10)) + '_e' + str(int(eps * 100)) + '.bson'
    print(f'Starts playing for {piece.__name__}, paramter = {parameter}, epoch = {epoch}')

    play = Play(filename, False, piece)
    win_rate, rounds = play.play_stats(games_to_play)
    
    result_dict[parameter, epoch] =  win_rate
    return result_dict


if __name__ == '__main__':
    base_memory = DIRECTORY_PATH + 'memory1-0-'
    games_to_play = 10000
    pieces = [Rook,Queen]
    list_epochs = [1000000,1500000,2000000,2500000,3000000,3500000,4000000,4500000,5000000]
    epsilons = [0.2,0.4,0.6,0.8]
    gamma = 0.8
    learning_rates = 0.8
    future_list = []
    for piece in pieces:
        with ProcessPoolExecutor(max_workers=6) as executor:
            for eps in epsilons:
                for epoch in list_epochs:
                    arguments = (base_memory, games_to_play, learning_rates, eps, piece, gamma, epoch, eps) #last argument is the parameter we are sweeping on 
                    future_list.append(executor.submit(calc_winrate, arguments)) 


        print("Joining for thread")


        merged_dict = {'piece' : piece.__name__, 'game_played' : games_to_play}
        for future in future_list:
            merged_dict.update(future.result())
        print(merged_dict)
        export_dict(merged_dict, f'win_rate_{piece.__name__}_eps02_to_08_ep_1_to_5.txt', mode = 'w')
