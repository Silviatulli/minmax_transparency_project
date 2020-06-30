import numpy as np
import random
from minmax import GameState, Action


class ChildQlearning(object):
    def __init__(self):
        num_states = (12 * 12)**2 * 2
        self.q_table = np.zeros((num_states, len(Action)))

    def Q(self, state, action):
        state_id = GameState.get_state_id(state)
        q_value = self.q_table[state_id, action]

        return q_value

    def policy(self, state):
        valid_actions = state.valid_actions()
        best_action = valid_actions[0]
        max_value = self.Q(state, best_action)
        epsilon = 0.15
        for action in valid_actions:
            if max_value < self.Q(state, action):
                max_value = self.Q(state, action)
                best_action = action

        best_actions = list()
        for action in valid_actions:
            if max_value == self.Q(state, action):
                best_actions.append(action)

        # choose the best action
        if np.random.rand() <= epsilon:
            idx = np.random.randint(len(valid_actions))
            action = valid_actions[idx]
        else:
            idx = np.random.randint(len(best_actions))
            action = best_actions[idx]

        return action

    def update(self, state, action, new_state):
        # reward function
        if state.get_score('child') < new_state.get_score('child'):
            reward = 1
        else:
            reward = -1

        # update q-table
        new_state_idx = GameState.get_state_id(new_state)
        alpha = 0.8
        gamma = 0.99
        V_star = np.max(self.q_table[new_state_idx, :])
        q_sa = self.Q(state, action)
        q_value = (1-alpha)*q_sa + alpha * (reward + gamma * V_star)

        state_id = GameState.get_state_id(state)

        self.q_table[state_id, action] = q_value

        return

    def demonstration_update(self, state, action, reward, new_state):
        # TODO: update the q-table when the robot makes an action
        # import robot decision
        # retrieve robot state, action and reward
        # translate the robot state, action and reward in useful
        # information (q values)
        # update q-table

        new_state_idx = GameState.get_state_id(new_state)
        alpha = 0.8
        gamma = 0.99
        q_value = (1-alpha)*self.Q(state, action) + alpha * \
            (reward + gamma * np.max(self.q_table[new_state_idx, :]))

        state_id = GameState.get_state_id(state)

        self.q_table[state_id, action] = q_value
        return

    def explanation_update(self, examples):
        return
