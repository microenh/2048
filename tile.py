import pygame

from constants import *

class Tile:
    
    def __init__(self, value: int, position: int):
        self.surf: pygame.Surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surf_rect: pygame.Rect = self.surf.get_rect()
        self.set_value(value)
        self.position = position
        self.row_vel = 0
        self.col_vel = 0
        self.row_ofs = 0
        self.col_ofs = 0

    def row_col(self) -> tuple[int, int]:
        return self.position // ROWS, self.position % ROWS, 
        
    def tile_rect(self) -> pygame.Rect:
        row, col = self.row_col()
        return pygame.Rect(
            (col * (TILE_WIDTH + DIVIDER_WIDTH) + DIVIDER_WIDTH
                 + self.col_ofs,
             row * (TILE_HEIGHT + DIVIDER_WIDTH) + DIVIDER_WIDTH
                 + self.row_ofs,
             TILE_WIDTH, TILE_HEIGHT))

    def set_value(self, value: int) -> None:
        self.value = value
        self.surf.fill(TILE_BG[self.value])
        pygame.draw.rect(self.surf, (0,0,0), self.surf_rect, width=1)
        text_surf: pygame.Surface = TEXT_FONT.render(f'{self.value}', True, TEXT_COLOR)
        text_rect: pygame.Rect = text_surf.get_rect(center = self.surf_rect.center)
        self.surf.blit(text_surf, text_rect)

    def update(self) -> None:
        if self.col_vel or self.row_vel:
            self.col_ofs += self.col_vel
            self.row_ofs += self.row_vel
            if self.row_ofs >= TILE_HEIGHT + DIVIDER_WIDTH:
                self.row_ofs = 0
                self.position += COLS
                self.row_vel = 0
            if self.row_ofs <= -TILE_HEIGHT - DIVIDER_WIDTH:
                self.row_ofs = 0
                self.position -= COLS
                self.row_vel = 0
            if self.col_ofs >= TILE_HEIGHT + DIVIDER_WIDTH:
                self.col_ofs = 0
                self.position += 1
                self.col_vel = 0
            if self.col_ofs <= -TILE_HEIGHT - DIVIDER_WIDTH:
                self.col_ofs = 0
                self.position -= 1
                self.col_vel = 0

    def __repr__(self) -> str:
        return f'{self.position}: {self.value}'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tile):
            return NotImplemented
        return self.value == other.value

    def render(self, display: pygame.Surface) -> None:
        display.blit(self.surf, self.tile_rect())
                
    
