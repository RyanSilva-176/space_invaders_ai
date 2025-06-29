# Imports
import pygame
import random
import sys
import math

# Importar de nossos módulos
from settings import *
from sprites import (
    Player,
    Bullet,
    PowerUp,
    Explosion,
)  # Invader e Barrier são criados por game_elements
from game_elements import create_invaders_for_level, create_barriers_for_level
from ui import display_text, show_screen_message

# --- Inicialização do Pygame ---
pygame.init()
pygame.mixer.init()  # Se for adicionar sons depois
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders Modular")
clock = pygame.time.Clock()

background_surface = pygame.Surface(screen.get_size()).convert()
background_surface.fill(BACKGROUND_COLOR)


# --- Loop Principal do Jogo ---
def game_loop():
    current_level = 1
    score = 0
    lives = PLAYER_LIVES_START

    running_game = True
    while running_game:
        # Grupos de Sprites
        all_sprites = pygame.sprite.Group()
        invaders_group = pygame.sprite.Group()
        bullets_group = pygame.sprite.Group()
        invader_bullets_group = pygame.sprite.Group()
        powerups_group = pygame.sprite.Group()
        barriers_group = pygame.sprite.Group()
        explosions_group = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

        create_barriers_for_level(all_sprites, barriers_group, current_level)
        create_invaders_for_level(all_sprites, invaders_group, current_level)

        invader_speed_current = 0.5 + (current_level * 0.2)
        invader_speed_current = min(invader_speed_current, 5)
        invader_move_direction = 1
        invader_base_shoot_chance = 0.001 + (current_level * 0.0005)
        invader_base_shoot_chance = min(invader_base_shoot_chance, 0.01)

        level_running = True
        while level_running:
            screen.blit(background_surface, (0, 0))

            # --- Eventos ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_game = False
                    level_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot(
                            all_sprites, bullets_group
                        )  # Passa os grupos necessários
                    if event.key == pygame.K_ESCAPE:
                        running_game = False
                        level_running = False

            # --- Atualizações ---
            all_sprites.update()

            # Movimento dos Invasores
            move_down = False
            for invader in invaders_group:
                invader.rect.x += invader_speed_current * invader_move_direction
                if invader.rect.right >= SCREEN_WIDTH - 10 or invader.rect.left <= 10:
                    move_down = True
            if move_down:
                invader_move_direction *= -1
                for inv in invaders_group:
                    inv.rect.y += INVADER_MOVE_DOWN_STEP
                    inv.rect.x += invader_speed_current * invader_move_direction

            # Invasores Atiram
            if invaders_group and random.random() < invader_base_shoot_chance * len(
                invaders_group
            ):
                shooters = [
                    inv
                    for inv in invaders_group
                    if inv.rect.bottom < player.rect.top - 50
                ]
                if shooters:
                    shooter = random.choice(shooters)
                    inv_bullet_speed = INVADER_BULLET_BASE_SPEED + (
                        current_level * 0.2
                    )  # Balas mais rápidas em níveis altos
                    inv_bullet = Bullet(
                        shooter.rect.centerx,
                        shooter.rect.bottom,
                        speed_y=inv_bullet_speed,
                        color=LIGHT_RED,
                    )
                    all_sprites.add(inv_bullet)
                    invader_bullets_group.add(inv_bullet)

            # Colisões: Balas do Jogador com Invasores
            for bullet in list(
                bullets_group
            ):  # Iterar sobre cópia se remover da lista original
                hits = pygame.sprite.spritecollide(bullet, invaders_group, False)
                for invader_hit in hits:
                    bullet.kill()
                    score_increase = invader_hit.points
                    is_destroyed_by_bullet = False

                    if bullet.bullet_type == "aoe":
                        explosion = Explosion(
                            invader_hit.rect.center, bullet.aoe_radius
                        )
                        all_sprites.add(explosion)
                        # Dano AoE imediato ao criar a explosão
                        for inv_in_radius in invaders_group:
                            dist = math.hypot(
                                inv_in_radius.rect.centerx - explosion.rect.centerx,
                                inv_in_radius.rect.centery - explosion.rect.centery,
                            )
                            if dist <= bullet.aoe_radius:
                                if inv_in_radius.get_hit(bullet.aoe_damage):
                                    score += inv_in_radius.points
                                    if (
                                        random.random()
                                        < INVADER_POWERUP_DROP_CHANCE_AOE
                                    ):
                                        ptype = random.choice(POWERUP_TYPES)
                                        powerup = PowerUp(
                                            inv_in_radius.rect.center, ptype
                                        )
                                        all_sprites.add(powerup)
                                        powerups_group.add(powerup)
                        # O invasor principal atingido pela bala AoE também precisa ser processado
                        if invader_hit.alive() and invader_hit.get_hit(
                            bullet.aoe_damage
                        ):  # Se ainda vivo e foi destruído
                            score += score_increase  # Contar pontos do alvo principal
                            if random.random() < INVADER_POWERUP_DROP_CHANCE_AOE:
                                ptype = random.choice(POWERUP_TYPES)
                                powerup = PowerUp(invader_hit.rect.center, ptype)
                                all_sprites.add(powerup)
                                powerups_group.add(powerup)

                    else:  # Bala normal
                        if invader_hit.get_hit(1):
                            is_destroyed_by_bullet = True
                            score += score_increase
                            if random.random() < INVADER_POWERUP_DROP_CHANCE_NORMAL:
                                ptype = random.choice(POWERUP_TYPES)
                                powerup = PowerUp(invader_hit.rect.center, ptype)
                                all_sprites.add(powerup)
                                powerups_group.add(powerup)
                    break  # Bala atinge um invasor ou inicia uma explosão

            # Colisões: Balas dos Invasores com Jogador
            player_bullet_hits = pygame.sprite.spritecollide(
                player, invader_bullets_group, True
            )
            if player_bullet_hits:
                if player.take_damage():
                    lives -= 1
                    if lives <= 0:
                        if not show_screen_message(
                            screen,
                            "GAME OVER",
                            f"Score Final: {score}",
                            "Pressione R para recomeçar ou Q para sair",
                            f"Alcançou o Nível: {current_level}",
                        ):
                            running_game = False
                        else:
                            current_level = 1
                            score = 0
                            lives = PLAYER_LIVES_START
                        level_running = False
                        continue

            # Colisões: Jogador com PowerUps
            collected_powerups = pygame.sprite.spritecollide(
                player, powerups_group, True
            )
            for pup in collected_powerups:
                player.activate_power_up(pup.type)

            # Colisões com Barreiras
            for barrier in barriers_group:
                barrier_player_bullet_hits = pygame.sprite.spritecollide(
                    barrier, bullets_group, True
                )
                for hit_bullet in barrier_player_bullet_hits:
                    barrier.hit(3 if hit_bullet.bullet_type == "aoe" else 1)

                barrier_invader_bullet_hits = pygame.sprite.spritecollide(
                    barrier, invader_bullets_group, True
                )
                for _ in barrier_invader_bullet_hits:
                    barrier.hit()

            # Game Over: Invasores chegam à base ou tocam o jogador
            for invader in invaders_group:
                if (
                    invader.rect.bottom >= player.rect.top - 10
                    or pygame.sprite.collide_rect(player, invader)
                ):
                    lives = 0
                    if not show_screen_message(
                        screen,
                        "GAME OVER",
                        f"Score Final: {score}",
                        "Pressione R para recomeçar ou Q para sair",
                        f"Alcançou o Nível: {current_level}",
                    ):
                        running_game = False
                    else:
                        current_level = 1
                        score = 0
                        lives = PLAYER_LIVES_START
                    level_running = False
                    break
            if not level_running:
                continue

            # Condição de Vitória do Nível
            if not invaders_group and level_running:
                current_level += 1
                if not show_screen_message(
                    screen,
                    f"NÍVEL {current_level-1} COMPLETO!",
                    f"Score: {score}",
                    "Pressione N para o Próximo Nível ou Q para Sair",
                    f"Indo para o Nível: {current_level}",
                ):
                    running_game = False
                level_running = False
                continue

            # --- Desenho ---
            all_sprites.draw(screen)
            display_text(screen, f"Score: {score}", 28, 10, 10, align="topleft")
            display_text(
                screen,
                f"Vidas: {lives}",
                28,
                SCREEN_WIDTH - 10,
                10,
                align="midtop",
                color=WHITE,
            )  # Ajuste para alinhar pela direita
            display_text(screen, f"Nível: {current_level}", 28, SCREEN_WIDTH / 2, 10)

            # Display de Power-ups ativos
            y_offset = 40
            if player.power_up_timers.get("attackspeed"):
                display_text(
                    screen, "ATK SPD+", 18, 10, y_offset, CYAN, align="topleft"
                )
                y_offset += 20
            if player.has_aoe_bullets:
                display_text(
                    screen, "BALAS AoE", 18, 10, y_offset, ORANGE, align="topleft"
                )
                y_offset += 20
            if player.has_shield:
                display_text(screen, "ESCUDO", 18, 10, y_offset, GOLD, align="topleft")

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()
q
