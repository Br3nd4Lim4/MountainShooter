import pygame.image
from pygame import Surface, Rect
from pygame.font import Font
from code.Const import WIN_WIDTH, MENU_OPTION, C_WHITE, C_YELLOW, C_ORANGE


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/MenuBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, "Mountain Shooter", C_ORANGE, ((WIN_WIDTH / 2), 35))

            menu_y = 135

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(18, MENU_OPTION[i], C_YELLOW, ((WIN_WIDTH / 2), menu_y + 25 * i))
                else:
                    self.menu_text(18, MENU_OPTION[i], C_WHITE, ((WIN_WIDTH / 2), menu_y + 25 * i))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0

                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1

                    if event.key == pygame.K_RETURN:
                        if MENU_OPTION[menu_option] == 'CONTROLS':
                            self.show_controls()
                        else:
                            return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        border_color = (0, 0, 0)
        border_surf: Surface = text_font.render(text, True, border_color).convert_alpha()
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in offsets:
            border_rect: Rect = border_surf.get_rect(center=(text_center_pos[0] + dx, text_center_pos[1] + dy))
            self.window.blit(source=border_surf, dest=border_rect)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

    def show_controls(self):
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(32, "CONTROLES", C_ORANGE, ((WIN_WIDTH / 2), 35))
            self.menu_text(22,"PLAYER 1", C_YELLOW, ((WIN_WIDTH / 2), 85))
            self.menu_text(18,"SETAS - MOVIMENTO", C_WHITE,((WIN_WIDTH / 2), 120))
            self.menu_text(18, "CTRL DIREITO - ATIRAR", C_WHITE, ((WIN_WIDTH / 2), 150))
            self.menu_text(22, "PLAYER 2", C_YELLOW, ((WIN_WIDTH / 2), 195))
            self.menu_text(18, "W A S D - MOVIMENTO", C_WHITE, ((WIN_WIDTH / 2), 230))
            self.menu_text(18, "CTRL ESQUERDO - ATIRAR", C_WHITE, ((WIN_WIDTH / 2), 260))
            self.menu_text(16, "ESC - VOLTAR AO MENU", C_WHITE, ((WIN_WIDTH / 2), 300))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
