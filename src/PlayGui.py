import os.path
from BaseParams import BoardPossitionParams
import pickle
import random
from Cheesboard import ChessBoard,King,Rook,Piece


class Play:

    def __init__(self,file_name):
        self.file_name = file_name
        self.R = self.load(file_name)


    def play(self, state_id=None):

        current_state_id = None
        turn = 0
        win = False

        if not  state_id:
            current_state_id = random.choice(list(self.R))
        else:
            current_state_id = state_id

        while True:

            if not current_state_id or turn >= 40:
                break

            board = get_board(current_state_id)

            if current_state_id[6] is 1:
                turn += 1

            next_states = self.R[current_state_id]

            if not next_states:
                board = get_board(current_state_id)

                if board.state == ChessBoard.BLACK_KING_CHECKMATE:
                    win = True
                break

            max_state_id = None
            if current_state_id[6] is 0:
                max_state_id = self.get_min_state(next_states)
                # max_state_id = random.choice(list(next_states.keys()))
            else:
                max_state_id = self.get_max_state(next_states)


            print ('Turn: ',turn)
            board.draw()
            for i in next_states:
                print (i,'->',next_states[i])
            print ('Max:', max_state_id,'->',next_states[max_state_id])
            input()

            current_state_id = max_state_id

        return win, turn

    @staticmethod
    def get_max_state(states):
        max_q = -1
        max_state = None

        # if random.random() < 0.1 :
        #    return random.choice(list(states.keys()))

        for state in states:

            if states[state] > max_q and states[state] != 0:
                max_q= states[state]
                max_state = state
            elif states[state] == 100:
                max_state = state
                break

        return max_state

    @staticmethod
    def get_min_state(states):
        min_q = 1
        min_state = None
        for state in states:

            if states[state] < min_q:
                min_q= states[state]
                min_state = state
            elif states[state] == -100:
                min_state = state
                break

        return min_state

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as infile:
            params = pickle.load(infile)
            return params


def get_board(state_id):
         wk_r, wk_c, wr_r, wr_c, bk_r, bk_c, white_plays = state_id
         return ChessBoard(wk=King(wk_r, wk_c, Piece.WHITE),
                            wr=Rook(wr_r, wr_c, Piece.WHITE),
                            bk=King(bk_r, bk_c, Piece.BLACK),
                            white_plays=white_plays,
                            debug=True
                            )
if __name__ == '__main__':

    p = Play('res/memory1-0_trained_5000000_6.bson')
    p.play()

