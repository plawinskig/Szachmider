import random

import pygame

def apply_crt_effect(screen):
    _apply_scanlines(screen)
    _apply_glow(screen)
    _apply_vhs_glitch(screen)

def _apply_scanlines(screen):
    width, height = screen.get_size()
    scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for y in range(0, height, 4):  # Every 4 pixels 
        pygame.draw.line(scanline_surface, (0, 0, 0, 60), (0, y), (width, y))  # Semi-transparent black

    screen.blit(scanline_surface, (0, 0))

def _apply_glow(screen):
    width, height = screen.get_size()

    # Create a blurred surface
    glow_surf = pygame.transform.smoothscale(screen, (width // 2, height // 2))
    glow_surf = pygame.transform.smoothscale(glow_surf, (width, height))

    # Overlay with transparency
    glow_surf.set_alpha(100)  # Adjust glow intensity (higher = stronger glow)
    screen.blit(glow_surf, (0, 0))

def _apply_vhs_glitch(screen):
    width, height = screen.get_size()
    glitch_surface = screen.copy()

    glitch_count = 1 # Adjust for glitch intensity

    for _ in range(glitch_count):
        _add_glitch_effect(height, width, glitch_surface)

    _add_rolling_static(screen, height, width)

    screen.blit(glitch_surface, (0, 0))

def _add_glitch_effect(height, width, glitch_surface):
    shift_amount = 5

    if random.random() < 0.1:
        y_start = random.randint(0, height - 20)
        slice_height = random.randint(5, 20)
        offset = random.randint(-shift_amount, shift_amount)

        slice_area = pygame.Rect(0, y_start, width, slice_height)
        slice_copy = glitch_surface.subsurface(slice_area).copy()
        glitch_surface.blit(slice_copy, (offset, y_start))


def _add_rolling_static(screen, height, width):
    static_chance = 0.1

    static_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(0, height, 8):
        if random.random() < static_chance:
            pygame.draw.line(static_surface, (255, 255, 255, random.randint(30, 80)), (0, y), (width, y))

    screen.blit(static_surface, (0, 0), special_flags=pygame.BLEND_ADD)
