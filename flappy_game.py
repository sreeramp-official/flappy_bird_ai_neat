import pygame  # Game library for drawing and handling events
import neat  # Library for NeuroEvolution of Augmenting Topologies
import os  # For interacting with the file system
import random  # For random number generation

# Initialize fonts in pygame
pygame.font.init()

# Set the width and height of the game window
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

# Global variable to keep track of generations in NEAT
generation_counter = 0

# Load and scale bird images for animation
BIRD_FRAMES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird3.png"))),
]

# Load and scale pipe, base, and background images
PIPE_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("assets", "pipe.png"))
)
GROUND_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("assets", "base.png"))
)
BACKGROUND_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("assets", "bg.png"))
)

# Set up the font for displaying score and generation
STAT_FONT = pygame.font.SysFont("comicsans", 50)


# ---------------- BIRD CLASS ----------------
class Bird:
    FRAMES = BIRD_FRAMES
    MAX_TILT = 25  # Max angle the bird can tilt upwards
    ROTATION_VELOCITY = 20  # How fast the bird tilts
    ANIMATION_DURATION = 5  # How long each bird frame is shown

    def __init__(self, x, y):
        self.x = x  # Bird's horizontal position
        self.y = y  # Bird's vertical position
        self.tilt = 0  # Bird's tilt angle
        self.tick_count = 0  # Time since last jump
        self.velocity = 0  # Bird's velocity
        self.height = self.y  # Initial height of bird
        self.frame_index = 0  # Animation frame index
        self.image = self.FRAMES[0]  # Current bird image

    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # Displacement equation: distance the bird moves this frame
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count**2

        if displacement >= 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2  # Faster upward motion

        self.y += displacement

        # Adjust tilt depending on bird's motion
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_TILT:
                self.tilt = self.MAX_TILT
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, window):
        self.frame_index += 1

        # Handle animation: flap up, middle, down, middle, repeat
        if self.frame_index <= self.ANIMATION_DURATION:
            self.image = self.FRAMES[0]
        elif self.frame_index <= self.ANIMATION_DURATION * 2:
            self.image = self.FRAMES[1]
        elif self.frame_index <= self.ANIMATION_DURATION * 3:
            self.image = self.FRAMES[2]
        elif self.frame_index <= self.ANIMATION_DURATION * 4:
            self.image = self.FRAMES[1]
        elif self.frame_index == self.ANIMATION_DURATION * 4 + 1:
            self.image = self.FRAMES[0]
            self.frame_index = 0

        if self.tilt <= -80:
            self.image = self.FRAMES[1]
            self.frame_index = self.ANIMATION_DURATION * 2

        # Rotate image based on tilt
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.x, self.y)).center
        )

        # Draw bird on window
        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        # Get mask for pixel-perfect collision
        return pygame.mask.from_surface(self.image)


# ---------------- PIPE CLASS ----------------
class Pipe:
    GAP = 200  # Vertical space between top and bottom pipes
    SPEED = 5  # Pipe movement speed

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.SPEED

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, window):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        top_collision = bird_mask.overlap(top_mask, top_offset)
        bottom_collision = bird_mask.overlap(bottom_mask, bottom_offset)

        return bool(top_collision or bottom_collision)


# ---------------- BASE (GROUND) CLASS ----------------
class Ground:
    SPEED = 5
    WIDTH = GROUND_IMAGE.get_width()
    IMAGE = GROUND_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        # Loop ground
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(self.IMAGE, (self.x1, self.y))
        window.blit(self.IMAGE, (self.x2, self.y))


# ---------------- DRAW GAME WINDOW ----------------
def draw_game_window(window, birds, pipes, ground, score, generation):
    window.blit(BACKGROUND_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw(window)

    # Draw score
    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(score_label, (WINDOW_WIDTH - 10 - score_label.get_width(), 10))

    # Draw generation number
    gen_label = STAT_FONT.render("Gen: " + str(generation), 1, (255, 255, 255))
    window.blit(gen_label, (10, 10))

    ground.draw(window)

    for bird in birds:
        bird.draw(window)

    pygame.display.update()


# ---------------- MAIN GAME FUNCTION FOR NEAT ----------------
def main(genomes, config):
    global generation_counter
    generation_counter += 1

    neural_nets = []
    genomes_list = []
    bird_list = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_nets.append(net)
        bird_list.append(Bird(230, 350))
        genome.fitness = 0
        genomes_list.append(genome)

    ground = Ground(730)
    pipes = [Pipe(600)]
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    running = True
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        pipe_index = 0
        if len(bird_list) > 0:
            if (
                len(pipes) > 1
                and bird_list[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
            ):
                pipe_index = 1
        else:
            break

        for i, bird in enumerate(bird_list):
            bird.move()
            genomes_list[i].fitness += 0.2

            # NEAT input: bird's height, distance to top and bottom pipe
            output = neural_nets[i].activate(
                (
                    bird.y,
                    abs(bird.y - pipes[pipe_index].height),
                    abs(bird.y - pipes[pipe_index].bottom),
                )
            )

            if output[0] > 0.5:
                bird.jump()

        add_new_pipe = False
        pipes_to_remove = []

        for pipe in pipes:
            for i, bird in enumerate(bird_list):
                if pipe.collide(bird, window):
                    genomes_list[i].fitness -= 1
                    bird_list.pop(i)
                    neural_nets.pop(i)
                    genomes_list.pop(i)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_new_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes_to_remove.append(pipe)

            pipe.move()

        if add_new_pipe:
            score += 1
            for genome in genomes_list:
                genome.fitness += 5
            pipes.append(Pipe(700))

        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        for i in reversed(range(len(bird_list))):
            bird = bird_list[i]
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                bird_list.pop(i)
                neural_nets.pop(i)
                genomes_list.pop(i)

        ground.move()
        draw_game_window(window, bird_list, pipes, ground, score, generation_counter)


# ---------------- NEAT CONFIGURATION AND RUNNER ----------------
def run_neat(config_file_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file_path,
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run for max 30 generations
    best_genome = population.run(main, 30)
    print("\nBest genome:\n", best_genome)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_feedforward.txt")
    run_neat(config_path)
