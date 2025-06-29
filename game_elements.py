# game_elements.py

import pygame
from settings import *
from sprites import Invader, Barrier  # Precisa das classes


def create_invaders_for_level(all_sprites_group, invaders_group, level):
    # Limpar invasores existentes (se houver, embora geralmente seja chamado em um novo nível)
    # for invader in invaders_group:
    #     invader.kill()

    rows = 4 + (level // 3)
    cols = 8 + (level // 2)
    rows = min(rows, 7)
    cols = min(cols, 12)

    for row_idx in range(rows):
        for col_idx in range(cols):
            invader_type = 1
            invader_health = 1
            if level >= 3 and row_idx < 1:
                invader_type = 2
                invader_health = 2
            elif level >= 5 and row_idx < 2:
                invader_type = 2
                invader_health = 2 + (level // 5)

            invader = Invader(
                INVADER_START_X_OFFSET + col_idx * INVADER_SPACING_X,
                INVADER_START_Y_OFFSET + row_idx * INVADER_SPACING_Y,
                invader_type,
                invader_health,
            )
            all_sprites_group.add(invader)
            invaders_group.add(invader)
    # Não precisamos retornar a matriz de invasores se não for usada externamente


def create_barriers_for_level(all_sprites_group, barriers_group, level):
    for b in barriers_group:
        b.kill()

    num_barriers = 4 - (level % 3)
    num_barriers = max(2, num_barriers)

    if num_barriers == 0:
        return

    barrier_width = SCREEN_WIDTH / (num_barriers * 2)
    barrier_spacing = (SCREEN_WIDTH - (num_barriers * barrier_width)) / (
        num_barriers + 1
    )
    y_pos = SCREEN_HEIGHT - BARRIER_Y_OFFSET - (level * 5 % BARRIER_LEVEL_Y_VARIATION)

    for i in range(num_barriers):
        x_pos = barrier_spacing + i * (barrier_width + barrier_spacing)
        barrier = Barrier(x_pos, y_pos, int(barrier_width), 30)
        all_sprites_group.add(barrier)
        barriers_group.add(barrier)
