import pygame
import random 

# Window dimensions
WIDTH = 400
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Bird dimensions
BIRD_RADIUS = 20

# Pipe dimensions
PIPE_WIDTH = 70
GAP_SIZE = 200
PIPE_SPEED = 3

class Bird:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = 0

    def update(self):
        self.y += self.velocity
        self.velocity += 1

    def jump(self):
        self.velocity = -10


class Pipe:
    def __init__(self, x):
        self.x = x
        self.delta = 50
        self.height = random.randint(
            HEIGHT / 4 - self.delta/2,
            HEIGHT / 4 + self.delta/2
        )  

    def update(self):
        self.x -= PIPE_SPEED


class Environment:
    def __init__(self):
        self.bird = Bird(WIDTH // 2, HEIGHT // 2, BIRD_RADIUS)
        self.pipes = [Pipe(WIDTH)]

        self.previous_score = 0
        self.current_score = 0

        self.previous_state = None
        self.current_state = None
        self.is_alive = True
        
        self.positive_reward = 10
        self.negative_reward = -500

    def get_state_labeled(self): 
        pipe_x = self.pipes[0].x + PIPE_WIDTH/2
        pipe_y = self.pipes[0].height

        pipe_low = [pipe_x, pipe_y + GAP_SIZE]
        pipe_high = [pipe_x, pipe_y]

        current_state = {
            "bird_y": self.bird.y, 
            "pipe_low": pipe_low, 
            "pipe_high": pipe_high, 
            "is_alive": self.is_alive
        }

        return current_state

    def reset(self):
        self.__init__()

        self.current_state = self.get_state_labeled()

        return self.current_state

    def update(self):
        self.bird.update()

        # Adding pipe as game progresses
        if self.pipes[-1].x < WIDTH - 200:
            self.pipes.append(Pipe(WIDTH))

        for pipe in self.pipes:
            if pipe.x + PIPE_WIDTH < self.bird.x:
                self.pipes.remove(pipe)

                self.current_score += 1
            pipe.update()

    def check_collision(self):
        # Bird's collision with floor and roof of screen
        if self.bird.y > HEIGHT or self.bird.y < 0:
            self.is_alive = False

        # Bird's collision with self.pipes
        for pipe in self.pipes:
            if pipe.x <= self.bird.x <= pipe.x + PIPE_WIDTH:
                if self.bird.y <= pipe.height or self.bird.y >= pipe.height + GAP_SIZE:
                    self.is_alive = False
    
    def get_reward(self):
        if (self.previous_state["is_alive"] == True) and (self.current_state["is_alive"] == False):
            return self.negative_reward

        if abs(self.current_score - self.previous_score) != 0:
            self.previous_score = self.current_score

            return self.positive_reward
        
        return 0
    
    def game_step(self, instruction):
        self.is_alive = True

        if instruction == 1:
            self.bird.jump()

        self.update()
        self.check_collision()

        # Feedback
        self.previous_state = self.current_state
        self.current_state = self.get_state_labeled()
        state = self.current_state

        reward = self.get_reward()

        # Returning relevant info
        return state, reward


# Things I stole from Andrew NG
import numpy as np
import tensorflow as tf

SEED = 0  # Seed for the pseudo-random number generator.
MINIBATCH_SIZE = 64  # Mini-batch size.
TAU = 1e-3  # Soft update parameter.
E_DECAY = 0.995  # ε-decay rate for the ε-greedy policy.
E_MIN = 0.01  # Minimum ε value for the ε-greedy policy.

def update_target_network(q_network, target_q_network):
    for target_weights, q_net_weights in zip(
        target_q_network.weights, q_network.weights
    ):
        target_weights.assign(TAU * q_net_weights + (1.0 - TAU) * target_weights)

def get_action(q_values, epsilon=0.0):
    if random.random() > epsilon:
        return np.argmax(q_values.numpy()[0])
    else:
        return random.choice([0, 1])

def check_update_conditions(t, num_steps_upd, memory_buffer):
    if (t + 1) % num_steps_upd == 0 and len(memory_buffer) > MINIBATCH_SIZE:
        return True
    else:
        return False

def get_experiences(memory_buffer):
    experiences = random.sample(memory_buffer, k=MINIBATCH_SIZE)
    states = tf.convert_to_tensor(
        np.array([e.state for e in experiences if e is not None]), dtype=tf.float32
    )
    actions = tf.convert_to_tensor(
        np.array([e.action for e in experiences if e is not None]), dtype=tf.float32
    )
    rewards = tf.convert_to_tensor(
        np.array([e.reward for e in experiences if e is not None]), dtype=tf.float32
    )
    next_states = tf.convert_to_tensor(
        np.array([e.next_state for e in experiences if e is not None]), dtype=tf.float32
    )
    is_alive_vals = tf.convert_to_tensor(
        np.array([e.is_alive for e in experiences if e is not None]).astype(np.uint8),
        dtype=tf.float32,
    )
    return (states, actions, rewards, next_states, is_alive_vals)

def get_new_eps(epsilon):
    return max(E_MIN, E_DECAY * epsilon)
