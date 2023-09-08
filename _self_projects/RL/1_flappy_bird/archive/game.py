import pygame
import random
import csv
import sys

random.seed(0)
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
GAP_SIZE = 300
PIPE_SPEED = 3

class Bird:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = 0

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), self.radius)

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
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + GAP_SIZE, PIPE_WIDTH, HEIGHT))

    def update(self):
        self.x -= PIPE_SPEED

def read_instructions(filename):
    instructions = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            instructions.extend(row)
    return instructions

def main():
    if len(sys.argv) < 2:
        print("Please provide a CSV file with instructions.")
        return

    instructions_file = sys.argv[1]
    instructions = read_instructions(instructions_file)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird = Bird(WIDTH // 2, HEIGHT // 2, BIRD_RADIUS)
    pipes = [Pipe(WIDTH)]

    running = True
    paused = False

    instruction_index = 0

    _ = 0
    while running:
        _ += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                elif event.key == pygame.K_p:
                    paused = not paused

        if paused:
            continue

        current_instruction = instructions[instruction_index]

        if _ % 20 == 0:
            bird.jump()

        bird.update()

        if pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe(WIDTH))

        for pipe in pipes:
            if pipe.x < -PIPE_WIDTH:
                pipes.remove(pipe)
            pipe.update()

        screen.fill(WHITE)

        for pipe in pipes:
            pipe.draw(screen)

        bird.draw(screen)

        if bird.y > HEIGHT or bird.y < 0:
            running = False

        for pipe in pipes:
            if pipe.x <= bird.x <= pipe.x + PIPE_WIDTH:
                if bird.y <= pipe.height or bird.y >= pipe.height + GAP_SIZE:
                    running = False

        pygame.display.flip()
        clock.tick(30)

        instruction_index += 1
        if instruction_index >= len(instructions):
            instruction_index = 0

    # Pause the game after the instructions have been completed
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                paused = False

if __name__ == '__main__':
    main()
