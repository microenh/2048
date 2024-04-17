#! /home/pi/Developer/2048/.venv/bin/python
import random
import pygame

from constants import *
from tile import Tile

class Main():
    def __init__(self) -> None:
        pygame.init()

        self.screen: pygame.Surface = pygame.display.set_mode(SCREEN_SIZE)
        self.screen_rect: pygame.Rect = self.screen.get_rect()
        self.running: bool = True
        logo: pygame.Surface = pygame.image.load('logo_small.png')
        pygame.display.set_icon(logo)
        pygame.display.set_caption('2048')
        self.setup_game_over()
        self.init_divider()
        self.fps: int = 0
        if SHOW_FPS:
            self.setup_fps()
##        self.tiles: list[Tile] = [Tile(4 << i, i) for i in range(16)]
        self.tiles: list[Tile] = []
        self.restart()
        self.run()

    def restart(self) -> None:
        self.go: bool = False
        self.score: int = 0
        self.move_ct: int = 0
        self.update_score(0)
        self.update_moves(0)
        self.high_tile: int = 0
        self.tiles.clear()
        for i in range(2):
            self.add_tile()

    def add_tile(self, value: int = 0) -> None:
        s: set[int] = set(range(ROWS*COLS))
        for tile in self.tiles:
            s.remove(tile.position)
        if value == 0:
            value = random.choice((2,4))
        self.tiles.append(Tile(value, random.choice(tuple(s))))
        self.update_high_tile(value)
            
    def merge_tiles(self, target: list[int], tiles: list[Tile]) -> tuple[list[Tile], bool]:
        moved = False
        dest:list[Tile] = []
        while len(tiles) >= 2:
            if tiles[0] == tiles[1]:
                moved = True
                tiles[0].set_value(new_value := tiles[0].value * 2)
                self.update_score(new_value)
                self.update_high_tile(new_value)
                dest.append(tiles[0])
                tiles = tiles[2:]
            else:
                dest.append(tiles[0])
                tiles = tiles[1:]
        if len(tiles) == 1:
            dest.append(tiles[0])
        for i, t in enumerate(dest):
            if t.position != target[i]:
                t.position = target[i]
                moved = True
        return dest, moved

    def do_move(self, key: int) -> bool:
        new_tiles = []
        moved = False
        d: dict[int, Tile] = {t.position: t for t in self.tiles}
        for target in MOVE_TARGET[key]:
            tiles: list[Tile] = [x for i in target if (x := d.get(i)) is not None]
            moved_tiles, m = self.merge_tiles(target, tiles)
            if m:
                moved = True
            new_tiles += moved_tiles
        self.tiles = new_tiles
        return moved

    def setup_game_over(self) -> None:
        go_surf: pygame.Surface = GO_FONT.render('Game Over', True, GO_COLOR)
        rect: pygame.Rect = go_surf.get_rect()
        rect = go_surf.get_rect()
        self.go_bg_rect = rect.copy()
        self.go_bg_rect.width += GO_FONT_SIZE
        self.go_bg_surf: pygame.Surface = pygame.Surface((self.go_bg_rect.width,
                                                         self.go_bg_rect.height))
        self.go_bg_surf.set_colorkey(TRANSPARENT)
        pygame.draw.rect(self.go_bg_surf,
                         GO_BG_COLOR,
                         self.go_bg_rect,
                         border_radius=GO_FONT_SIZE)
        rect.center = self.go_bg_rect.center
        self.go_bg_surf.blit(go_surf, rect)
        self.go_bg_rect.center = self.screen_rect.center
        

    def setup_fps(self) -> None:
        fps_metrics: list[tuple[int,int,int,int,int]] = FPS_FONT.metrics('0')
        
        self.fps_border_surf: pygame.Surface = pygame.Surface(
            (2 * fps_metrics[0][1] + 20, FPS_FONT_SIZE))
        self.fps_border_surf.set_colorkey(TRANSPARENT)
        self.fps_border_rect: pygame.Rect = self.fps_border_surf.get_rect()
        pygame.draw.rect(self.fps_border_surf,
                         FPS_BORDER_COLOR,
                         self.fps_border_rect,
                         border_radius=FPS_FONT_SIZE)
        self.fps_border_rect.right = SCREEN_SIZE[0] - FPS_OFFSET
        self.fps_border_rect.bottom = SCREEN_SIZE[1] - FPS_OFFSET

        self.update_fps()
        self.fps_timer: int = pygame.event.custom_type()
        pygame.time.set_timer(self.fps_timer, 1000)
        self.divider.blit(self.fps_border_surf, self.fps_border_rect)

    def init_divider(self) -> None:
        self.divider: pygame.Surface = pygame.Surface(SCREEN_SIZE)
        self.divider.fill(DIVIDER_COLOR)
        self.divider.set_colorkey(TRANSPARENT)
        rect: pygame.Rect = self.screen_rect
        pygame.draw.lines(self.divider, DIVIDER_HILIGHT, False,
                          ((rect.left, rect.bottom),
                           (rect.left, rect.top),
                           (rect.right, rect.top)), width=1)
        pygame.draw.lines(self.divider, DIVIDER_SHADOW, False,
                          ((rect.left, rect.bottom-1),
                           (rect.right-1, rect.bottom-1),
                           (rect.right-1, rect.top)), width=1)

        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(
                    (col * (TILE_WIDTH + DIVIDER_WIDTH) + DIVIDER_WIDTH,
                     row * (TILE_HEIGHT + DIVIDER_WIDTH) + DIVIDER_WIDTH,
                     TILE_WIDTH, TILE_HEIGHT))
                pygame.draw.rect(self.divider, TRANSPARENT, rect)
                rect.inflate_ip((2,2))
                pygame.draw.lines(self.divider, DIVIDER_SHADOW, False,
                                  ((rect.left, rect.bottom),
                                   (rect.left, rect.top),
                                   (rect.right, rect.top)), width=1)
                pygame.draw.lines(self.divider, DIVIDER_HILIGHT, False,
                                  ((rect.left, rect.bottom),
                                   (rect.right, rect.bottom),
                                   (rect.right, rect.top)), width=1)
                
        legend_surf: pygame.Surface = SCORE_FONT.render('Score:', True, SCORE_COLOR)
        rect = legend_surf.get_rect(left = SCORE_LEFT, top = SCORE_TOP)
        self.divider.blit(legend_surf, rect)
        legend_surf = SCORE_FONT.render('Moves:', True, SCORE_COLOR)
        rect = legend_surf.get_rect(left = SCORE_LEFT, top = MOVES_TOP)
        self.divider.blit(legend_surf, rect)
        legend_surf = SCORE_FONT.render('High Tile:', True, SCORE_COLOR)
        rect = legend_surf.get_rect(left = SCORE_LEFT, top = HIGH_TOP)
        self.divider.blit(legend_surf, rect)
        legend_surf = SCORE_FONT.render('q: QUIT,    r: RESET', True, SCORE_COLOR)
        rect = legend_surf.get_rect(center = self.screen_rect.center,
                                    bottom = self.screen_rect.bottom - KEYS_V_OFFSET)
        self.divider.blit(legend_surf, rect)

    def update_fps(self) -> None:
        self.fps_surf = FPS_FONT.render(f'{self.fps:2}', True, FPS_COLOR)
        self.fps_rect = self.fps_surf.get_rect(
            center=self.fps_border_rect.center)
        self.fps = 0

    def update_score(self, value: int) -> None:
        self.score += value
        self.score_surf: pygame.Surface = SCORE_FONT.render(f'{self.score}', True, SCORE_COLOR)
        self.score_rect: pygame.Rect = self.score_surf.get_rect(right = SCORE_RIGHT,
                                                                top = SCORE_TOP)

    def update_moves(self, moves:int = 1) -> None:
        self.move_ct += moves
        self.move_surf: pygame.Surface = SCORE_FONT.render(f'{self.move_ct}', True, SCORE_COLOR)
        self.move_rect: pygame.Rect = self.move_surf.get_rect(right = SCORE_RIGHT,
                                                              top = MOVES_TOP)

    def update_high_tile(self, value: int) -> None:
        if value > self.high_tile:
            self.high_tile = value
            self.high_surf: pygame.Surface = SCORE_FONT.render(f'{value}', True, SCORE_COLOR)
            self.high_rect: pygame.Rect = self.high_surf.get_rect(right = SCORE_RIGHT,
                                                                   top = HIGH_TOP)
            
    def event_loop(self) -> None:
        self.fps += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif SHOW_FPS and event.type == self.fps_timer:
                self.update_fps()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN, pygame.K_UP,
                                 pygame.K_LEFT, pygame.K_RIGHT):
                    if self.do_move(event.key):
                        self.update_moves()
                        self.add_tile()
                    elif len(self.tiles) == ROWS*COLS:
                        self.go = True
                elif event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.restart()

    def update(self) -> None:
        for tile in self.tiles:
            tile.update()

    def render(self) -> None:
        self.screen.fill(BG_COLOR)
        for tile in self.tiles:
            tile.render(self.screen)
        self.screen.blit(self.divider, self.screen_rect)
        if SHOW_FPS:
            self.screen.blit(self.fps_surf, self.fps_rect)
        
        self.screen.blit(self.score_surf, self.score_rect)
        self.screen.blit(self.move_surf, self.move_rect)
        self.screen.blit(self.high_surf, self.high_rect)
        if self.go:
            self.screen.blit(self.go_bg_surf, self.go_bg_rect)

        
    def run(self) -> None:
        clock: pygame.time.Clock = pygame.time.Clock()
        while self.running:
            self.event_loop()
            self.update()
            self.render()
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()
        

if __name__ == '__main__':
    Main()
