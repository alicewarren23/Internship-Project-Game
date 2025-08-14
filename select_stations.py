import pygame
import sys

pygame.init()
bg = pygame.image.load("Internship/Tube_Map.jpeg")
bg_rect = bg.get_rect()
WIDTH, HEIGHT = bg_rect.size

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Select Tube Stations")

stations = []

font = pygame.font.SysFont(None, 24)
instructions = font.render("Click to select tube stations. Press ENTER to finish.", True, (0, 0, 0))

running = True
finished = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not finished:
            pos = pygame.mouse.get_pos()
            stations.append(pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                finished = True

    screen.blit(bg, (0, 0))
    screen.blit(instructions, (10, 10))
    for station in stations:
        pygame.draw.circle(screen, (255, 0, 0), station, 8)
    pygame.display.flip()

pygame.quit()
print("Station coordinates:", stations)