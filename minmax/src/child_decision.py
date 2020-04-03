import numpy as np
from game_model import GameState



class Child(object):
    #TODO: 
    #      Representation of relevant data:
    #      q table
    #
    #      Things your code needs to be able to do:(features)
    #      ability to update the child
    #      perform an action

    def __init__(self):
        num_states = (12 * 12)**2 * 2
        self.q_table = np.zeros((num_states, 16))

    def Q(self, state, action):
        action_name, ball_id = action
        action_id = GameState.get_action_id(action_name, ball_id)
        state_id = GameState.get_state_id(state)
        q_value = self.q_table[state_id, action_id]
    
        return q_value

    def policy(self, state):
        valid_actions = state.valid_actions()
        best_action = valid_actions[0]
        max_value = self.Q(state, best_action)
        for action in valid_actions:
            if max_value < self.Q(state, action):
                max_value = self.Q(state, action)
                best_action = action

        best_actions = list()
        for action in valid_actions:
            if max_value == self.Q(state, action):
                best_actions.append(action)

        idx = np.random.randint(len(best_actions))
        return best_actions[idx]
    
    def update(self, state, action, new_state):
        # reward function
        if state.get_score('child') < new_state.get_score('child'):
            reward = 1
        else:
            reward = -1

        # import pdb; pdb.set_trace()

        # update q-table
        new_state_idx = GameState.get_state_id(new_state)
        alpha = 0.8
        gamma = 0.99
        q_value = (1-alpha)*self.Q(state,action) + alpha * (reward + gamma * np.max(self.q_table[new_state_idx, :]))
        
        state_id = GameState.get_state_id(state)
        action_name, ball_id = action
        action_id = GameState.get_action_id(action_name, ball_id)
        
        self.q_table[state_id, action_id] = q_value
        print(q_value)
        
        return
