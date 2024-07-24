import numpy as np
import random

class DiceGame:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        self.total = self.dice1 + self.dice2
        self.state = self.total - 2  # Map the sum (2 to 12) to state index (0 to 10)
        return self.state
    
    def step(self, action):
        reward = 0
        if action == 0:  # Guess number
            if self.total == 7:
                reward = 1
            done = True
        elif action == 1:  # Ask higher than a number
            number = random.randint(1, 12)
            if self.total > number:
                reward = 0.1
            done = False
        elif action == 2:  # Ask lower than a number
            number = random.randint(1, 12)
            if self.total < number:
                reward = 0.1
            done = False
        else:
            raise ValueError("Invalid action")
        
        return self.state, reward, done
    
    def render(self):
        print(f"Dice1: {self.dice1}, Dice2: {self.dice2}, Total: {self.total}")

class QLearningAgent:
    def __init__(self, state_space, action_space, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995, min_exploration_rate=0.01):
        self.state_space = state_space
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.q_table = np.zeros((state_space, action_space))
        
    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.action_space - 1)
        else:
            return np.argmax(self.q_table[state])
        
    def learn(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error
        
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
        
    def train(self, env, episodes):
        for episode in range(episodes):
            state = env.reset()
            done = False
            while not done:
                action = self.choose_action(state)
                next_state, reward, done = env.step(action)
                self.learn(state, action, reward, next_state)
                state = next_state
                if done:
                    print(f"Episode {episode + 1}: Total = {env.total}, Action = {action}, Reward = {reward}")
            if (episode + 1) % 100 == 0:
                print(f"Episode {episode + 1}: Exploration rate = {self.exploration_rate}")

if __name__ == "__main__":
    env = DiceGame()
    state_space = 11  # Sum of two dice ranges from 2 to 12 (indexing 0 to 10)
    action_space = 3  # Three possible actions
    agent = QLearningAgent(state_space, action_space)
    
    agent.train(env, episodes=1000)
    
    env.render()
