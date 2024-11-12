import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Multiple Instances of Bacteria and Virus with Disappearing Animation")

# Load images
image1 = pygame.image.load("bacteria_placeholder.png")  # Stationary bacteria image
image3 = pygame.image.load("virus_placeholder.png")     # Stationary virus image
image2 = pygame.image.load("macrophage_placeholder.png")  # Movable macrophage image

# Resize images to a smaller size
image1 = pygame.transform.scale(image1, (60, 60))  # Resize bacteria to 60x60
image3 = pygame.transform.scale(image3, (60, 60))  # Resize virus to 60x60
image2 = pygame.transform.scale(image2, (80, 80))   # Resize macrophage to 80x80

# Create lists to store bacteria and virus instances
bacteria_list = []
virus_list = []

# Number of bacteria and viruses
num_bacteria = 10
num_viruses = 10

# Randomly position bacteria and viruses
for _ in range(num_bacteria):
    # Random x, y position for bacteria within screen bounds
    x_pos = random.randint(50, 700)
    y_pos = random.randint(50, 500)
    rect = image1.get_rect(topleft=(x_pos, y_pos))
    bacteria_list.append({"rect": rect, "disappearing": False, "disappear_time": 0, "shrink_factor": 1})

for _ in range(num_viruses):
    # Random x, y position for virus within screen bounds
    x_pos = random.randint(50, 700)
    y_pos = random.randint(50, 500)
    rect = image3.get_rect(topleft=(x_pos, y_pos))
    virus_list.append({"rect": rect, "disappearing": False, "disappear_time": 0, "shrink_factor": 1})

# Get rectangle for the movable macrophage image
rect2 = image2.get_rect()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear screen
    screen.fill((0, 0, 0))  # Black background

    # Update rect2 position based on mouse position for demo purposes
    rect2.center = pygame.mouse.get_pos()

    # Check for collision with bacteria and viruses
    for bacteria in bacteria_list[:]:
        if bacteria["rect"].colliderect(rect2):  # If macrophage collides with bacteria
            if not bacteria["disappearing"]:
                bacteria["disappearing"] = True
                bacteria["disappear_time"] = pygame.time.get_ticks()  # Start disappear timer

    for virus in virus_list[:]:
        if virus["rect"].colliderect(rect2):  # If macrophage collides with virus
            if not virus["disappearing"]:
                virus["disappearing"] = True
                virus["disappear_time"] = pygame.time.get_ticks()  # Start disappear timer

    # Animate the shrinking effect for bacteria
    for bacteria in bacteria_list:
        if bacteria["disappearing"]:
            time_since_collision = pygame.time.get_ticks() - bacteria["disappear_time"]
            if time_since_collision < 500:  # Shrink over 500ms
                bacteria["shrink_factor"] = 1 - (time_since_collision / 500)
            else:
                bacteria_list.remove(bacteria)  # Remove bacteria after shrinking animation is done

        # Draw bacteria with shrink factor if still present
        if not bacteria["disappearing"]:
            screen.blit(image1, bacteria["rect"])  # Draw bacteria
        else:
            # Draw the shrinking bacteria image
            new_size = int(60 * bacteria["shrink_factor"])
            shrinked_image = pygame.transform.scale(image1, (new_size, new_size))
            new_rect = shrinked_image.get_rect(center=bacteria["rect"].center)
            screen.blit(shrinked_image, new_rect)

    # Animate the shrinking effect for viruses
    for virus in virus_list:
        if virus["disappearing"]:
            time_since_collision = pygame.time.get_ticks() - virus["disappear_time"]
            if time_since_collision < 500:  # Shrink over 500ms
                virus["shrink_factor"] = 1 - (time_since_collision / 500)
            else:
                virus_list.remove(virus)  # Remove virus after shrinking animation is done

        # Draw virus with shrink factor if still present
        if not virus["disappearing"]:
            screen.blit(image3, virus["rect"])  # Draw virus
        else:
            # Draw the shrinking virus image
            new_size = int(60 * virus["shrink_factor"])
            shrinked_image = pygame.transform.scale(image3, (new_size, new_size))
            new_rect = shrinked_image.get_rect(center=virus["rect"].center)
            screen.blit(shrinked_image, new_rect)

    # Always draw the movable image (macrophage)
    screen.blit(image2, rect2)

    # Update display
    pygame.display.flip()
