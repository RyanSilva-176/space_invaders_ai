import pygame
import sys  # Para sys.exit() nas telas de mensagem
from settings import *


def display_text(surface, text, size, x, y, color=WHITE, align="midtop"):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if align == "midtop":
        text_rect.midtop = (x, y)
    elif align == "topleft":
        text_rect.topleft = (x, y)
    elif align == "midbottom":
        text_rect.midbottom = (x, y)
    # Adicione mais alinhamentos se necessário

    surface.blit(text_surface, text_rect)


def show_screen_message(screen, main_text, score_text, instruction_text, level_text=""):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    display_text(
        screen,
        main_text,
        64,
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT / 4 - (30 if level_text else 0),
    )
    if level_text:
        display_text(screen, level_text, 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 40)
    display_text(screen, score_text, 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    display_text(screen, instruction_text, 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if (
                    event.key == pygame.K_r or event.key == pygame.K_n
                ):  # N para próximo nível
                    return True  # Indica que o jogador quer continuar/reiniciar
        pygame.time.Clock().tick(FPS // 2)  # Reduzir FPS nas telas de mensagem
    return False  # Nunca deveria chegar aqui se Q ou R/N são pressionados
