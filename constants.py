import pygame

pygame.init()

SCREEN_DIM: int = 800
LEGEND_V: int = 200

SCREEN_SIZE: tuple[int, int] = (SCREEN_DIM, SCREEN_DIM + LEGEND_V)

DIVIDER_COLOR: pygame.Color = pygame.Color('burlywood3')
DIVIDER_HILIGHT: pygame.Color = pygame.Color('burlywood2')
DIVIDER_SHADOW: pygame.Color = pygame.Color('burlywood4')
DIVIDER_WIDTH: int = 11

ROWS: int = 4
COLS: int = 4
TILE_WIDTH = (SCREEN_DIM - (ROWS + 1) * DIVIDER_WIDTH) // COLS
TILE_HEIGHT = (SCREEN_DIM - (COLS + 1) * DIVIDER_WIDTH) // ROWS
FPS: int = 8

BG_COLOR: pygame.Color = pygame.Color('burlywood1')

TEXT_COLOR: pygame.Color = pygame.Color('azure4')
TEXT_FONT: pygame.font.Font = pygame.font.Font(None, 256 // COLS)

FPS_FONT_SIZE: int = SCREEN_DIM // 20
FPS_OFFSET: int = FPS_FONT_SIZE // 2
FPS_FONT: pygame.font.Font = pygame.font.Font(None, FPS_FONT_SIZE)
FPS_COLOR: pygame.Color = pygame.Color('gray60')
FPS_BORDER_COLOR: pygame.Color = pygame.Color('gray30')
TRANSPARENT: pygame.Color = pygame.Color((0,0,0))
SHOW_FPS: bool = False

SCORE_FONT_SIZE: int = SCREEN_DIM // 20
SCORE_FONT: pygame.font.Font = pygame.font.Font(None, SCORE_FONT_SIZE)
SCORE_COLOR: pygame.Color = pygame.Color('gray90')
SCORE_LEFT: int = DIVIDER_WIDTH
SCORE_TOP: int = SCREEN_DIM + 8
MOVES_TOP: int = SCORE_TOP + SCORE_FONT_SIZE
HIGH_TOP: int = MOVES_TOP + SCORE_FONT_SIZE
SCORE_RIGHT: int = 300
KEYS_V_OFFSET: int = 4

GO_FONT_SIZE: int = SCREEN_DIM // 8
GO_FONT: pygame.font.Font = pygame.font.Font(None, GO_FONT_SIZE)
GO_COLOR: pygame.Color = pygame.Color('yellow')
GO_BG_COLOR: pygame.Color = pygame.Color('blue')


MOVE_TARGET: dict[int, list[list[int]]] = {
    pygame.K_LEFT: [[col + row * COLS for col in range(COLS)]
        for row in range(ROWS)],
    pygame.K_RIGHT: [[col + row * COLS for col in range(COLS-1,-1,-1)]
        for row in range(ROWS)],
    pygame.K_UP: [[col + row * COLS for row in range(ROWS)]
        for col in range(COLS)],
    pygame.K_DOWN: [[col + row * COLS for row in range(ROWS-1,-1,-1)]
        for col in range(COLS)]
}

TILE_BG = {
         2: (237, 229, 218),
         4: (238, 225, 201),
         8: (243, 178, 122),
        16: (246, 150, 101),
        32: (247, 124,  95),
        64: (247,  95,  59),
       128: (237, 208, 115),
       256: (237, 204,  99),
       512: (236, 202,  80),
      1024: (237, 229, 218),
      2048: (238, 225, 201),
      4096: (243, 178, 122),
      8192: (246, 150, 101),
     16384: (247, 124,  95),
     32768: (247,  95,  59),
     65536: (237, 208, 115),
    131072: (237, 204,  99),
}

