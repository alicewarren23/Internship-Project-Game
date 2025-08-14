import pygame
import sys
import os
import random
from branches import branch_stack  # Import dictionary from branches.py

pygame.init()
pygame.font.init()

# Load background image
bg_path = os.path.join(os.path.dirname(__file__), "Tube_Map.jpeg")
if not os.path.exists(bg_path):
    print("Background image not found:", bg_path)
    sys.exit()
bg = pygame.image.load(bg_path)
bg_rect = bg.get_rect()
WIDTH, HEIGHT = bg_rect.size

# Display setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball on Tube Map")

# Load train image
train_img_path = os.path.join(os.path.dirname(__file__), "toy-train.png")
if not os.path.exists(train_img_path):
    print("Train image not found:", train_img_path)
    sys.exit()
train_img = pygame.image.load(train_img_path)
train_img = pygame.transform.scale(train_img, (50, 50))
train_rect = train_img.get_rect()
train_width, train_height = train_rect.size

# Load confetti image
confetti_img_path = os.path.join(os.path.dirname(__file__), "Confetti.png")
if not os.path.exists(confetti_img_path):
    print("Confetti image not found:", confetti_img_path)
    sys.exit()
confetti_img = pygame.image.load(confetti_img_path)
confetti_img = pygame.transform.scale(confetti_img, (200, 200))  # Made twice as big

# Convert dict to lists
path_names = list(branch_stack.keys())
paths = list(branch_stack.values())

# Start on main path
current_path_idx = path_names.index("main_path")
current_path = paths[current_path_idx]
ball_pos_idx = 0
ball_x, ball_y = current_path[ball_pos_idx]

clock = pygame.time.Clock()

# Define your specific junctions with the paths they connect
junctions = {
    (134, 242): [path_names.index("main_path"), path_names.index("old_data_street")],
    (351, 297): [path_names.index("main_path"), path_names.index("assumption_circus")],
    (220, 256): [path_names.index("main_path"), path_names.index("shared_drive_central")],
    (522, 183): [path_names.index("main_path"), path_names.index("validata_cross")],  # Changed from 521 to 522
    (727, 305): [path_names.index("main_path"), path_names.index("mail_end")],
    (522, 199): [path_names.index("main_path"), path_names.index("biasminster")]
}

print("Junctions configured:")
for coord, path_indices in junctions.items():
    path_names_at_junction = [path_names[i] for i in path_indices]
    print(f"  {coord}: {path_names_at_junction}")

# Path name → label
name_to_label = {
    "main_path": "Continue",
    "old_data_street": "To Old Data Street",
    "assumption_circus": "To Assumption Circus",
    "shared_drive_central": "To Shared Drive Central",
    "validata_cross": "To Validata Cross",
    "mail_end": "To Mail End",
    "biasminster": "To Biasminster"
}

btn_colors = [
    (0, 0, 255), (0, 128, 0), (128, 0, 128),
    (255, 165, 0), (255, 0, 255), (255, 215, 0),
    (0, 255, 255)
]

def show_popup(screen, options, current_path_name):
    popup_width, popup_height = 700, 250
    popup = pygame.Surface((popup_width, popup_height))
    popup.fill((173, 216, 230))
    pygame.draw.rect(popup, (0, 0, 0), popup.get_rect(), 3)

    font = pygame.font.SysFont(None, 22)
    title_font = pygame.font.SysFont(None, 32)
    
    title_text = title_font.render(f"Junction ahead!" , True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(popup_width // 2, 30))
    popup.blit(title_text, title_rect)
    
    subtitle_text = font.render("Choose your path:", True, (0, 0, 0))
    subtitle_rect = subtitle_text.get_rect(center=(popup_width // 2, 60))
    popup.blit(subtitle_text, subtitle_rect)

    buttons = []
    btn_width = 180
    btn_height = 100
    start_x = (popup_width - (len(options) * btn_width + (len(options) - 1) * 20)) // 2
    
    for i, path_idx in enumerate(options):
        label = name_to_label.get(path_names[path_idx], f"Path {path_idx}")
        
        # Create button background
        btn_x = start_x + i * (btn_width + 20)
        btn_y = 100
        btn_color = btn_colors[i % len(btn_colors)]
        
        pygame.draw.rect(popup, btn_color, (btn_x, btn_y, btn_width, btn_height))
        pygame.draw.rect(popup, (0, 0, 0), (btn_x, btn_y, btn_width, btn_height), 2)
        
        # Add text to button
        btn_text = font.render(label, True, (255, 255, 255))
        text_rect = btn_text.get_rect(center=(btn_x + btn_width // 2, btn_y + btn_height // 2))
        popup.blit(btn_text, text_rect)
        
        buttons.append((btn_x, btn_x + btn_width, btn_y, btn_y + btn_height, path_idx))

    # Center popup on screen
    popup_x = WIDTH // 2 - popup_width // 2
    popup_y = HEIGHT // 2 - popup_height // 2
    screen.blit(popup, (popup_x, popup_y))
    pygame.display.flip()

    choosing = True
    choice = None
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for bx1, bx2, by1, by2, path_idx in buttons:
                    if popup_x + bx1 < mx < popup_x + bx2 and popup_y + by1 < my < popup_y + by2:
                        choice = path_idx
                        choosing = False
        pygame.time.wait(50)
    return choice

def return_to_main_path():
    """Find the nearest junction on main path and return there"""
    main_path_idx = path_names.index("main_path")
    main_path = paths[main_path_idx]
    
    # Find all junction coordinates that are on the main path
    main_junctions = []
    for junction_coord in junctions.keys():
        if junction_coord in main_path:
            main_junctions.append(junction_coord)
    
    if main_junctions:
        # For simplicity, return to the first junction on main path
        # You could make this smarter by finding the closest one
        target_coord = main_junctions[0]
        target_pos = main_path.index(target_coord)
        return main_path_idx, target_pos, target_coord
    else:
        # If no junctions found, return to start of main path
        return main_path_idx, 0, main_path[0]

branch_history = []

# Add this new function after your other helper functions
def find_previous_junction(current_path, current_pos_idx):
    """Find the last junction we passed on the current path"""
    # Look backwards through the path from current position
    for i in range(current_pos_idx, -1, -1):
        coord = current_path[i]
        if coord in junctions:
            return i, coord
    return 0, current_path[0]  # Return start if no junction found

# Confetti class
class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(2, 5)
        self.angle = random.randint(0, 360)

confetti_particles = []
showing_confetti = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RIGHT]:
        if ball_pos_idx < len(current_path) - 1:
            previous_pos = (ball_x, ball_y)
            ball_pos_idx += 1
            ball_x, ball_y = current_path[ball_pos_idx]
            
            print(f"DEBUG: Moving from {previous_pos} to ({ball_x}, {ball_y})")
            print(f"DEBUG: Current path: {path_names[current_path_idx]}")
            if (ball_x, ball_y) in junctions:
                print(f"DEBUG: Found junction! Available paths: {[path_names[i] for i in junctions[(ball_x, ball_y)]]}")
            
            # Check if current position is a junction
            if (ball_x, ball_y) in junctions:
                options = junctions[(ball_x, ball_y)]
                current_path_name = name_to_label[path_names[current_path_idx]]
                
                print(f"*** JUNCTION DETECTED at ({ball_x}, {ball_y}) ***")
                print(f"Available paths: {[path_names[i] for i in options]}")
                
                choice = show_popup(screen, options, current_path_name)
                
                if choice is not None:
                    if choice == current_path_idx:
                        # If choosing to continue on same path, just increment position
                        if ball_pos_idx < len(current_path) - 1:
                            ball_pos_idx += 1
                            ball_x, ball_y = current_path[ball_pos_idx]
                            print(f"Continuing on {path_names[current_path_idx]}")
                    else:
                        # Save current state to history and switch paths
                        branch_history.append((current_path_idx, ball_pos_idx))
                        current_path_idx = choice
                        current_path = paths[current_path_idx]
                        
                        # Find position on new path
                        if (ball_x, ball_y) in current_path:
                            ball_pos_idx = current_path.index((ball_x, ball_y))
                        else:
                            ball_pos_idx = 0
                        ball_x, ball_y = current_path[ball_pos_idx]
                        print(f"Switched to {path_names[current_path_idx]} at position {ball_pos_idx}")
            else:
                print(f"No junction at ({ball_x}, {ball_y})")
        else:
            print(f"Reached end of {path_names[current_path_idx]} - use LEFT arrow to backtrack or SPACEBAR to return to main path")
        pygame.time.wait(120)

    if keys[pygame.K_LEFT]:
        if ball_pos_idx > 0:
            ball_pos_idx -= 1
            ball_x, ball_y = current_path[ball_pos_idx]
            
            print(f"Moved back to position ({ball_x}, {ball_y}) on {path_names[current_path_idx]}")
            
            # Check if we've backtracked to a junction
            if (ball_x, ball_y) in junctions:
                options = junctions[(ball_x, ball_y)]
                
                # If we're on a branch path and the junction connects to main_path, offer to return
                main_path_idx = path_names.index("main_path")
                if current_path_idx != main_path_idx and main_path_idx in options:
                    print(f"*** JUNCTION DETECTED while backtracking at ({ball_x}, {ball_y}) ***")
                    print(f"Available paths: {[path_names[i] for i in options]}")
                    
                    current_path_name = name_to_label[path_names[current_path_idx]]
                    choice = show_popup(screen, options, current_path_name)
                    
                    if choice is not None:
                        # Save current state to history
                        branch_history.append((current_path_idx, ball_pos_idx))
                        
                        # Switch to chosen path
                        current_path_idx = choice
                        current_path = paths[current_path_idx]
                        
                        # Find position on new path (should be the same junction coordinate)
                        if (ball_x, ball_y) in current_path:
                            ball_pos_idx = current_path.index((ball_x, ball_y))
                        else:
                            # If junction coordinate not found, start at beginning of path
                            ball_pos_idx = 0
                        ball_x, ball_y = current_path[ball_pos_idx]
                        
                        print(f"Switched back to {path_names[current_path_idx]} at position {ball_pos_idx}")
            else:
                print(f"No junction at ({ball_x}, {ball_y}) while backtracking")
        else:
            print(f"Cannot move further back on {path_names[current_path_idx]} - at start of path")
        pygame.time.wait(120)

    if keys[pygame.K_BACKSPACE]:
        if branch_history:
            prev_path_idx, prev_pos_idx = branch_history.pop()
            current_path_idx = prev_path_idx
            current_path = paths[current_path_idx]
            ball_pos_idx = prev_pos_idx
            ball_x, ball_y = current_path[ball_pos_idx]
            print(f"Returned to {path_names[current_path_idx]} at position {ball_pos_idx}")
        pygame.time.wait(200)

    # NEW: SPACEBAR to return to main path
    if keys[pygame.K_SPACE]:
        # Find the previous junction on current path
        prev_junction_idx, prev_junction_coord = find_previous_junction(current_path, ball_pos_idx)
        
        if prev_junction_idx != ball_pos_idx:  # Only move if we're not already at a junction
            ball_pos_idx = prev_junction_idx
            ball_x, ball_y = prev_junction_coord
            
            # Switch to main path if we're at a junction that connects to it
            if (ball_x, ball_y) in junctions:
                main_path_idx = path_names.index("main_path")
                if main_path_idx in junctions[(ball_x, ball_y)]:
                    # Switch to main path
                    current_path_idx = main_path_idx
                    current_path = paths[current_path_idx]
                    
                    # Find the correct position on the main path
                    ball_pos_idx = current_path.index((ball_x, ball_y))
                    
                    # Verify we can move forward
                    if ball_pos_idx < len(current_path) - 1:
                        print(f"*** SPACEBAR PRESSED - Returned to main path at junction ({ball_x}, {ball_y}). Can continue forward! ***")
                    else:
                        print(f"*** SPACEBAR PRESSED - Warning: At end of main path! ***")
                    
                    # Add to branch history
                    branch_history.append((current_path_idx, ball_pos_idx))
                else:
                    print(f"*** SPACEBAR PRESSED - At junction ({ball_x}, {ball_y}) but no main path connection ***")
            else:
                print(f"*** SPACEBAR PRESSED - Returned to position ({ball_x}, {ball_y}) ***")
        else:
            print("Already at a junction!")
        pygame.time.wait(300)

    # Check if train reached the target point
    if (ball_x, ball_y) == (835, 232) and not showing_confetti:
        showing_confetti = True
        # Create new confetti particles
        for _ in range(50):  # Reduced number of pieces since they're bigger
            confetti_particles.append(
                Confetti(
                    random.randint(0, WIDTH),
                    random.randint(-50, 0)
                )
            )

    # Update and draw confetti
    if showing_confetti:
        for particle in confetti_particles[:]:
            particle.y += particle.speed
            particle.angle += 2
            if particle.y > HEIGHT:
                particle.y = random.randint(-50, 0)
                particle.x = random.randint(0, WIDTH)
            
            # Rotate and draw confetti
            rotated_confetti = pygame.transform.rotate(confetti_img, particle.angle)
            screen.blit(rotated_confetti, (particle.x, particle.y))

    screen.blit(bg, (0, 0))
    screen.blit(train_img, (ball_x - train_width // 2, ball_y - train_height // 2))

    if showing_confetti:
        for particle in confetti_particles[:]:
            particle.y += particle.speed
            particle.angle += 2
            if particle.y > HEIGHT:
                particle.y = random.randint(-50, 0)
                particle.x = random.randint(0, WIDTH)
            
            # Rotate and draw confetti
            rotated_confetti = pygame.transform.rotate(confetti_img, particle.angle)
            screen.blit(rotated_confetti, (particle.x, particle.y))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()