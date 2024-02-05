import random
from BaseParams import BoardPossitionParams, BoardPossitionParamsKQ, DIRECTORY_PATH
import time
from multiprocessing import Process

class QLearning:
    """
    The QLearning class
    """

    def __init__(self, params, gamma, learning_rate, epochs, eps, name):
        self.params = params
        self.epochs = epochs
        self.file_name = name
        self.gamma = gamma
        self.R = self.params.load(name)
        self.all_params = list(self.R.keys())
        self.learning_rate = learning_rate
        self.eps = eps

    def learning(self, epochs=None):
        """
        Actual learning function. All learning take place here.
        :param epochs: Number of episodes to run algorithm for
        :return: Algorithm runtime
        """
        last = time.time()

        if not epochs:
            epochs = self.epochs

        # Choose random initial state
        current_state_id = random.choice(self.all_params)

        # List of all positions visited in current episode
        visited_pos = []

        while epochs > 0:

            # All possible actions for current state. Basically next possible states of chessboard
            possible_states = self.R[current_state_id]

            # If is checkmate, draw or loos state it doesn`t have any next possible states so end episode.
            # Also ends episode if it visits previously visited position
            # if not possible_states or current_state_id in visited_pos:
            if not possible_states:
                epochs -= 1
                # if (epochs % 10000) == 0:
                #     print(epochs)

                # Select new initial state for episode
                current_state_id = random.choice(self.all_params)
                visited_pos = []
                # Start new episode

                continue

            if random.random() <= self.eps:
                # Select random action for for current state
                rnd_action_id = random.choice(list(possible_states.keys()))
            else:
                rnd_action_id = self._get_max(current_state_id)
                if rnd_action_id is None:
                    rnd_action_id = random.choice(list(possible_states.keys()))

            visited_pos.append(current_state_id)
            # Do learning step
            current_state_id = self._cal_learning_step(current_state_id, rnd_action_id)


        now = time.time()
        return now - last

    def _cal_learning_step(self, state, next_state):
        mx = 0
        poss_actions = self.R[next_state]

        white_plays = state[6]
        if white_plays == 1:
            mx = 1
        else:
            mx = 0

        non_zero = False
        # Looking for min action for White and max for Black
        for a in poss_actions:
            if white_plays == 1 and poss_actions[a] != -1 and poss_actions[a] <= mx:
                non_zero = True
                mx = poss_actions[a]
            if white_plays == 0 and poss_actions[a] != -1 and poss_actions[a] >= mx:
                non_zero = True
                mx = poss_actions[a]

        # If min/max not initial was found update Q value
        if non_zero:
            r_curr = self.R[state][next_state]
            self.R[state][next_state] = r_curr + self.learning_rate * (mx * self.gamma - r_curr)

        return next_state

    def _get_max(self, state):
        poss_actions = self.R[state]

        white_plays = state[6]
        if white_plays == 1:
            mx = 0
        else:
            mx = 1

        max_action = None

        for a in poss_actions:
            if white_plays == 1 and poss_actions[a] != -1 and poss_actions[a] >= mx:
                max_action = a
                mx = poss_actions[a]
            if white_plays == 0 and poss_actions[a] != -1 and poss_actions[a] <= mx:
                max_action = a
                mx = poss_actions[a]

        return max_action

    def save(self):

        file = self.file_name.split('.')[0] + '_Q_trained_ep' + str(self.epochs) + '_g' + str(int(self.gamma * 100)) + \
               '_l' + str(int(self.learning_rate * 10)) + '_e' + str(int(self.eps * 100)) + '.bson'

        print('Memory Saved:', file)
        self.params.save(self.R, file)


if __name__ == '__main__':
    pieces_setup_rook = BoardPossitionParams()
    pieces_setup_queen = BoardPossitionParamsKQ()
    setups, files = [pieces_setup_rook,pieces_setup_queen],['memory1-0-Rook.bson','memory1-0-Queen.bson']
    epsilons = [0.2,0.4,0.6,0.8]
    list_epochs = [1000000,1500000,2000000,2500000,3000000,3500000,4000000,4500000,5000000]
    # gammas = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,]
    # epsilons = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    for setup, file in zip(setups, files):
        for epoch in list_epochs:
            for l_r in epsilons:
                # for eps in epsilons:
                q = QLearning(setup, gamma=0.8, learning_rate = l_r, epochs=epoch, eps=0.9, name=DIRECTORY_PATH + file)

                last = time.time()
                ttime = q.learning()
                print('Time:', ttime)
                q.save()