import numpy as np
import gym
from gym import spaces


class MnkEnv(gym.Env):

    def __init__(self, m=3, n=3, k=3, p=2):
        self.board_length = m
        self.board_width = n
        self.empty_symbol = 0
        self.streak_to_win = k  # how many consecutive symbols (horizontally/vertically/diagonally) required to win
        self.num_players = p
        self.player = 1  # starting player
        self.num_filled_slots = 0
        self.board = self.reset()
        self.reward = 0
        self.info = {}
        self.done = 0
        self.action_space = spaces.Discrete(self.board_length * self.board_width)
        self.observation_space = spaces.Box(low=0, high=self.num_players,
                                            shape=(self.board_length, self.board_width), dtype=np.uint8)

    def reset(self):
        return [[self.empty_symbol for _ in range(self.board_width)] for _ in range(self.board_length)]

    def step(self, action):
        row = int(action / self.board_width)
        column = action - row * self.board_width
        print(action)
        if self.board[row][column] != self.empty_symbol:  # illegal move
            self.reward = -float('inf')
        else:
            self.num_filled_slots += 1
            self.board[row][column] = self.player
            if self.is_done():
                self.done = 1
                self.reward = 1
            elif self.num_filled_slots == self.board_length * self.board_width:
                self.done = 1
                self.reward = 0
            if self.done:
                if self.reward:
                    print("WINNER: Player {}.".format(self.player))
                else:
                    print("DRAWN GAME!")
            self.player = self.player % self.num_players + 1

        return self.board, self.reward, self.info, self.done

    def is_done(self):
        for i in range(self.board_length):
            for j in range(self.board_width):
                if self.board[i][j] == self.player:
                    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
                    for delta in deltas:
                        if self.check(i, j, self.streak_to_win - 1, delta, {}):
                            return True
        return False

    def check(self, i, j, k, delta, visited):
        solution = False
        if k == 0:
            self.board[i][j] = '*'+str(self.board[i][j])+'*'
            return True
        if 0 <= i + delta[0] < self.board_length and 0 <= j + delta[1] < self.board_width and \
                (i + delta[0], j + delta[1]) not in visited and \
                self.board[i + delta[0]][j + delta[1]] == self.player:
            visited[(i + delta[0], j + delta[1])] = True
            solution |= self.check(i + delta[0], j + delta[1], k - 1, delta, visited)
            if solution:
                self.board[i][j] = '*'+str(self.board[i][j])+'*'
                return True
        return solution

    def render(self, mode='human', close=False):
        for i in range(self.board_length):
            row = ''
            for j in range(self.board_width):
                row += '%3s | ' % str(self.board[i][j])
            print(row, "\n")
        print("===============================")


if __name__ == '__main__':
    T = MnkEnv(4, 6, 3)
    while not T.done:
        T.step(np.random.randint(T.board_length * T.board_width))
        T.render()