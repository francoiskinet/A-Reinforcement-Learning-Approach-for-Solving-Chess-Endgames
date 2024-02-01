import matplotlib.pyplot as plt
import numpy as np
import ast

def import_dict(nom_de_fichier):
    dictionnaire = {}
    with open(nom_de_fichier, 'r') as fichier:
        for ligne in fichier:
            cle, valeur = ligne.strip().split(': ')
            if '(' in cle:
                dictionnaire[ast.literal_eval(cle)] = valeur
            else:
                 dictionnaire[cle] = valeur
    return dictionnaire




if __name__ == '__main__':
    parameter = 'learning rate'
    filename = 'win_rate_Rook_lr02_to_08_ep_1_to_5.txt'
    dict_datas = import_dict(filename)
    game_played = dict_datas.pop("game_played")
    piece = dict_datas.pop("piece")
    figure_title = f"Win percentage of a {piece} in {game_played} games \n versus epochs for different {parameter}"
    figure_name =  f'win_rate_{piece}_{parameter}_vs_epoch.png'
    labels = "learning rate ="
    
    
    new_dict = {}
    plt.figure()
    for key, value in dict_datas.items():
        if key[0] in new_dict:
            new_dict[key[0]].append([key[1], value])
        else:
            new_dict[key[0]] = [[key[1], value]]
    plt.figure(figsize=(8,6))
    for key, value in new_dict.items():
        datas = np.array(new_dict[key], dtype=np.float64)
        plt.plot(datas.T[0], datas.T[1], '.', label = labels + str(key) )    
    plt.title(figure_title)
    plt.xlabel('Epochs')
    plt.ylabel('Win rate')
    # start, end = plt.ylim()  # get the current limits
    # step_size = (end - start) / 5  # adjust this value to get the desired number of ticks
    # plt.yticks(np.arange(start, end, step_size))
    plt.legend()
    plt.savefig(figure_name, dpi=200)


