# sprites.py

import pygame
import random
from settings import *  # Importa todas as configurações


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image_orig = pygame.image.load(PLAYER_IMG_PATH).convert_alpha()
        self.image = pygame.Surface([50, 30])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = PLAYER_START_X
        self.rect.bottom = SCREEN_HEIGHT - PLAYER_START_Y_OFFSET
        self.speed_x = 0

        self.base_shoot_delay = PLAYER_BASE_SHOOT_DELAY
        self.shoot_delay = self.base_shoot_delay
        self.last_shot = pygame.time.get_ticks()

        self.has_aoe_bullets = False
        self.has_shield = False
        self.power_up_timers = {}
        self.power_up_duration = PLAYER_POWERUP_DURATION

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -PLAYER_SPEED
        if keystate[pygame.K_RIGHT]:
            self.speed_x = PLAYER_SPEED

        self.rect.x += self.speed_x

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self._check_power_up_timers()

    def _check_power_up_timers(self):
        now = pygame.time.get_ticks()
        active_powerups_changed = False
        for p_type in list(
            self.power_up_timers.keys()
        ):  # Iterar sobre uma cópia das chaves
            if now > self.power_up_timers[p_type]:
                if p_type == "attackspeed":
                    self.shoot_delay = self.base_shoot_delay
                elif p_type == "aoe":
                    self.has_aoe_bullets = False
                elif p_type == "shield":
                    self.has_shield = False
                    self.image.fill(GREEN)  # Volta à cor normal
                del self.power_up_timers[p_type]
                active_powerups_changed = True
        # Opcional: adicionar uma flag se a interface precisar ser redesenhada especificamente
        # if active_powerups_changed: print(f"Power-up {p_type} expirou.")

    def shoot(self, all_sprites_group, bullets_group):  # Renomeado para evitar conflito
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet_type = "aoe" if self.has_aoe_bullets else "normal"
            bullet = Bullet(self.rect.centerx, self.rect.top, bullet_type=bullet_type)
            all_sprites_group.add(bullet)
            bullets_group.add(bullet)

    def activate_power_up(self, type):
        now = pygame.time.get_ticks()
        self.power_up_timers[type] = now + self.power_up_duration

        if type == "attackspeed":
            self.shoot_delay = self.base_shoot_delay // 2
        elif type == "aoe":
            self.has_aoe_bullets = True
        elif type == "shield":
            self.has_shield = True
            self.image.fill(GOLD)

    def take_damage(self):
        if self.has_shield:
            self.has_shield = False
            self.image.fill(GREEN)
            if "shield" in self.power_up_timers:
                del self.power_up_timers["shield"]
            return False  # Não perdeu vida
        return True  # Perdeu vida


class Invader(pygame.sprite.Sprite):
    def __init__(self, x, y, invader_type=1, health=1):
        super().__init__()
        self.invader_type = invader_type
        # self.image_orig = pygame.image.load(INVADER1_IMG_PATH if invader_type == 1 else INVADER2_IMG_PATH).convert_alpha()
        self.image = pygame.Surface([40, 30])
        if self.invader_type == 1:
            self.image.fill(RED)
            self.points = INVADER_POINTS_TYPE1
        else:
            self.image.fill(BLUE)
            self.points = INVADER_POINTS_TYPE2
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health

    def get_hit(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True  # Destruído
        return False  # Ainda vivo


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self, x, y, speed_y=PLAYER_BULLET_SPEED, color=YELLOW, bullet_type="normal"
    ):
        super().__init__()
        self.bullet_type = bullet_type
        self.aoe_radius = AOE_BULLET_RADIUS
        self.aoe_damage = AOE_BULLET_DAMAGE

        if self.bullet_type == "aoe":
            self.image = pygame.Surface([8, 20])
            self.image.fill(ORANGE)
        else:
            self.image = pygame.Surface([5, 15])
            self.image.fill(color)

        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.speed_y = speed_y
        self.color = color

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center_pos, type):
        super().__init__()
        self.type = type
        # self.image_orig = pygame.image.load(f"powerup_{type}.png").convert_alpha()
        self.image = pygame.Surface([25, 25])
        if type == "attackspeed":
            self.image.fill(CYAN)
        elif type == "aoe":
            self.image.fill(ORANGE)
        elif type == "shield":
            self.image.fill(MAGENTA)
        self.rect = self.image.get_rect(center=center_pos)
        self.speed_y = POWERUP_SPEED_Y

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, radius):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, ORANGE, (radius, radius), radius)
        self.rect = self.image.get_rect(center=center)
        self.spawn_time = pygame.time.get_ticks()
        self.duration = AOE_EXPLOSION_DURATION

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > self.duration:
            self.kill()


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, width=60, height=30):
        super().__init__()
        self.max_health = BARRIER_MAX_HEALTH
        self.health = self.max_health
        self.base_image = pygame.Surface([width, height])
        self.base_image.fill(DARK_GREEN)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))

    def hit(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.kill()
        else:
            damage_ratio = self.health / self.max_health
            new_g = int(50 + 100 * damage_ratio)
            self.image.fill((0, max(0, new_g), 0))
