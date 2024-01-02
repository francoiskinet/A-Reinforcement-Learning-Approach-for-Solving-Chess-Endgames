
from Play import Play
from BaseParams import FILE_PATH


if __name__ == '__main__':
    filename = FILE_PATH + '\memory1-0-KQ_Q_trained_ep1000000_g99_l8_e90.bson'
    epoch = 1000000
    gamma = 0.99
    learning_rate = 0.8
    eps = 0.9

    games_to_play = 1000

    base_memory = filename
    fp = base_memory.split('.')[0] + '_Q_trained_ep' + str(epoch) + '_g' + str(int(gamma * 100)) + \
               '_l' + str(int(learning_rate * 10)) + '_e' + str(int(eps * 100)) + '.bson'

    play = Play(fp, False)
    wins, rounds = play.play_stats(games_to_play)

    print('Win perc:', wins,'Average Rounds:', rounds)
