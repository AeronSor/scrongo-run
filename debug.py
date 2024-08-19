import pygame

pygame.init()
font = pygame.font.Font(None, 10)


def debug(info, x=10, y=10):
    """This function will display any kind of information in real time without
    looping with the main game loop"""
    display_surface = pygame.display.get_surface()
    debug_surface = font.render(str(info), True, 'Black')
    debug_rect = debug_surface.get_rect(topleft=(x, y))
    display_surface.blit(debug_surface, debug_rect)
