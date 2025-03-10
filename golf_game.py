import pygame
import math
import time
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Precision Drive Golf")

# Colors (retro style)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
DARK_GREEN = (0, 80, 0)  # For grass texture
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game variables
BALL_START_X, BALL_START_Y = 100, 500  # Tee position
HOLE_X, HOLE_Y = 600, 200              # Hole position
CONTROL_SENSITIVITY = 10               # Left/Right movement
DRIFT_FACTOR = 0.9                     # Drift momentum (90% of previous velocity)
POWER_BOOST = 1.7                      # Up arrow/W lift
POWER_DROP = 1.2                       # Down arrow/S reduction
state = "instructions"                 # States: "instructions", "setup", "flight", "landed"
ball_x, ball_y = BALL_START_X, BALL_START_Y
ball_vx, ball_vy = 0, 0                # Ball velocity (vx now includes drift)
ball_h_drift = 0                       # Horizontal drift velocity
power = 0                              # Swing power
timer_start = 0                        # Timer
landed_time = 0                        # Time at landing
distance_to_hole = 0                   # Distance feedback
first_input = False                    # Track first arrow key press

# Font for text
font = pygame.font.Font(None, 36)

# Generate static grass texture (squares)
GRASS_SIZE = 10  # Size of each square
grass_patches = [(random.randint(0, WIDTH - GRASS_SIZE), random.randint(0, HEIGHT - GRASS_SIZE)) for _ in range(150)]

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    # Draw textured grass background
    screen.fill(GREEN)
    for patch_x, patch_y in grass_patches:
        pygame.draw.rect(screen, DARK_GREEN, (patch_x, patch_y, GRASS_SIZE, GRASS_SIZE))

    # Draw hole (yellow circle with red flag)
    pygame.draw.circle(screen, YELLOW, (HOLE_X, HOLE_Y), 10)
    pygame.draw.line(screen, RED, (HOLE_X, HOLE_Y), (HOLE_X, HOLE_Y - 20), 3)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if state == "instructions" and event.key == pygame.K_RETURN:
                state = "setup"  # Start game
            elif state == "setup" and event.key == pygame.K_SPACE:
                power = min(power + 10, 100)  # Charge power
            elif state == "landed" and event.key == pygame.K_RETURN:
                # Reset to instructions
                ball_x, ball_y = BALL_START_X, BALL_START_Y
                ball_vx, ball_vy = 0, 0
                ball_h_drift = 0
                power = 0
                first_input = False
                state = "instructions"
        if event.type == pygame.KEYUP and state == "setup" and event.key == pygame.K_SPACE:
            # Launch ball with initial velocity
            ball_vx = power * 0.2 + 3  # Forward speed
            ball_vy = -power * 0.1     # Upward lift
            timer_start = time.time()
            state = "flight"

    # State: Instructions
    if state == "instructions":
        instructions = [
            "Instructions:",
            "SPACE: Swing from the tee",
            "LEFT/A: Move left",
            "RIGHT/D: Move right",
            "UP/W: Add lift",
            "DOWN/S: Drop lower",
            "Press ENTER to start"
        ]
        for i, line in enumerate(instructions):
            text = font.render(line, True, WHITE)
            screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 100 + i * 40))

    # State: Setup
    if state == "setup":
        pygame.draw.circle(screen, WHITE, (BALL_START_X, BALL_START_Y - 20), 10)  # Golfer head
        pygame.draw.line(screen, WHITE, (BALL_START_X, BALL_START_Y - 20), (BALL_START_X, BALL_START_Y), 3)  # Golfer body
        power_bar = pygame.Rect(50, 50, power * 2, 20)
        pygame.draw.rect(screen, RED, power_bar)  # Power meter
        text = font.render("Hold SPACE to swing", True, WHITE)
        screen.blit(text, (50, 80))

    # State: Flight
    if state == "flight":
        # Update ball position
        ball_x += ball_vx + ball_h_drift  # Include drift
        ball_y += ball_vy

        # Arrow key and WASD controls
        keys = pygame.key.get_pressed()
        input_active = False  # Track if any key is pressed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ball_h_drift -= CONTROL_SENSITIVITY  # Push left
            input_active = True
            first_input = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ball_h_drift += CONTROL_SENSITIVITY  # Push right
            input_active = True
            first_input = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            ball_vy = -POWER_BOOST  # Lift
            input_active = True
            first_input = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            ball_vy = POWER_DROP  # Drop
            input_active = True
            first_input = True

        # Apply drift (slowly decays)
        ball_h_drift *= DRIFT_FACTOR

        # Only land if no input AND first input has occurred
        if not input_active and first_input:
            landed_time = time.time()
            distance_to_hole = math.sqrt((ball_x - HOLE_X) ** 2 + (ball_y - HOLE_Y) ** 2) / 4  # Scaled to meters
            if math.sqrt((ball_x - HOLE_X) ** 2 + (ball_y - HOLE_Y) ** 2) < 2.5:
                distance_to_hole = 0.0
            state = "landed"

        # Keep ball within screen bounds during flight
        if ball_y < 0: ball_y = 0
        if ball_x < 0: ball_x = 0
        if ball_x > WIDTH: ball_x = WIDTH

        # Draw ball
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), 5)

        # Timer display
        elapsed_time = time.time() - timer_start
        timer_text = font.render(f"Time: {elapsed_time:.2f}s", True, WHITE)
        screen.blit(timer_text, (WIDTH - 150, 20))

    # State: Landed
    if state == "landed":
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), 5)  # Ball stays visible
        time_taken = landed_time - timer_start
        result_text = font.render(f"Time: {time_taken:.2f}s  Distance: {distance_to_hole:.1f}m", True, WHITE)
        screen.blit(result_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
        retry_text = font.render("Press ENTER to retry", True, WHITE)
        screen.blit(retry_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))

        # Check for perfect hole-in-one
        if distance_to_hole < 0.1:
            congrats_text = font.render(f"Congratulations! Time: {time_taken:.2f}s", True, YELLOW)
            screen.blit(congrats_text, (WIDTH // 2 - 180, HEIGHT // 2 - 60))

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()