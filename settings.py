import pygame

# --- Constantes de Tela e Jogo ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# --- Cores ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)  # Player
DARK_GREEN = (0, 100, 0)  # Barreiras
RED = (200, 0, 0)  # Invader tipo 1
BLUE = (0, 0, 200)  # Invader tipo 2
YELLOW = (255, 255, 0)  # Player Bullet
LIGHT_RED = (255, 100, 100)  # Invader Bullet
CYAN = (0, 255, 255)  # Power-up Attack Speed
ORANGE = (255, 165, 0)  # Power-up AoE / Explosão
MAGENTA = (255, 0, 255)  # Power-up Shield
GOLD = (255, 215, 0)  # Cor do escudo ativo
BACKGROUND_COLOR = (20, 20, 40)  # Azul escuro espacial

# --- Configurações do Jogador ---
PLAYER_START_X = SCREEN_WIDTH // 2
PLAYER_START_Y_OFFSET = 20
PLAYER_SPEED = 7
PLAYER_BASE_SHOOT_DELAY = 300  # Milissegundos
PLAYER_POWERUP_DURATION = 7000  # 7 segundos
PLAYER_LIVES_START = 3

# --- Configurações dos Invasores ---
INVADER_START_X_OFFSET = 50
INVADER_START_Y_OFFSET = 50
INVADER_SPACING_X = 50
INVADER_SPACING_Y = 40
INVADER_MOVE_DOWN_STEP = 15
INVADER_POINTS_TYPE1 = 10
INVADER_POINTS_TYPE2 = 25
INVADER_POWERUP_DROP_CHANCE_NORMAL = 0.10  # 10%
INVADER_POWERUP_DROP_CHANCE_AOE = 0.15  # 15% (quando destruído por AoE)

# --- Configurações das Balas ---
PLAYER_BULLET_SPEED = -10
INVADER_BULLET_BASE_SPEED = 4
AOE_BULLET_RADIUS = 50
AOE_BULLET_DAMAGE = 1
AOE_EXPLOSION_DURATION = 150  # Milissegundos

# --- Configurações das Barreiras ---
BARRIER_MAX_HEALTH = 5
BARRIER_Y_OFFSET = 150
BARRIER_LEVEL_Y_VARIATION = 50

# --- Configurações de Power-up ---
POWERUP_SPEED_Y = 2
POWERUP_TYPES = ["attackspeed", "aoe", "shield"]

# --- Fontes (opcional, pode ser None para padrão) ---
FONT_NAME = None  # pygame.font.match_font('arial')

# --- Caminhos de Assets (se você for usar imagens/sons) ---
# PLAYER_IMG_PATH = "assets/images/player.png"
# INVADER1_IMG_PATH = "assets/images/invader1.png"
# ... e assim por diante
