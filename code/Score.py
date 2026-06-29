import sys
from datetime import datetime
from pygame.font import Font
import pygame
from pygame import Surface, Rect, KEYDOWN, K_RETURN, K_BACKSPACE, K_ESCAPE
from code.Const import C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE, WIN_WIDTH, WIN_HEIGHT, C_CYAN, C_ORANGE
from code.DBProxy import DBProxy


class Score:
    def __init__(self, window: Surface):
        self.window = window
        self.surf = pygame.image.load('./asset/ScoreBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        pass

    def save(self, game_mode: str, player_score: list[int]):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy('DBScore')
        name = ''

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.score_text(48, 'VOCE VENCEU!!!', C_YELLOW, SCORE_POS['Title'])
            text = 'Insira o nome do jogador 1 (4 caracteres):'
            score = player_score[0]

            if game_mode == MENU_OPTION[0]:
                score = player_score[0]

            if game_mode == MENU_OPTION[1]:
                score = (player_score[0] + player_score[1]) / 2
                text = 'Insira nome do time (4 caracteres):'

            if game_mode == MENU_OPTION[2]:
                if player_score[0] >= player_score[1]:
                    score = player_score[0]
                else:
                    score = player_score[1]
                    text = 'Insira nome do jogador 2 (4 caracteres):'

            self.score_text(20, text, C_WHITE, SCORE_POS['EnterName'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return

                    if event.key == K_RETURN and len(name) == 4:
                        db_proxy.save({'name': name, 'score': score, 'date': get_formatted_date()})
                        self.show()
                        return
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 4:
                            name += event.unicode
            self.score_text(20, name, C_WHITE, SCORE_POS['Name'])
            if len(name) == 4:
                self.score_text(16, "PRESSIONE ENTER PARA SALVAR", C_YELLOW, (WIN_WIDTH / 2, SCORE_POS['Name'][1] + 35))
            else:
                self.score_text(14, "ESC - CANCELAR E VOLTAR", C_WHITE, (WIN_WIDTH / 2, WIN_HEIGHT - 30))
            pygame.display.flip()
            pass

    def show(self):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        self.window.blit(source=self.surf, dest=self.rect)
        self.score_text(48, 'TOP 10 SCORE', C_ORANGE, SCORE_POS['Title'])

        x_nome = 120
        x_pontos = 250
        x_data = 390
        y_label = SCORE_POS['Label'][1]

        self.score_text(20, 'NOME', C_ORANGE, (x_nome, y_label), align="left")
        self.score_text(20, 'PONTOS', C_ORANGE, (x_pontos, y_label), align="left")
        self.score_text(20, 'DATA', C_ORANGE, (x_data, y_label), align="left")

        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for player_score in list_score:
            id_, name, score, date = player_score
            y_pos = SCORE_POS[list_score.index(player_score)][1]
            self.score_text(20, f'{name}', C_YELLOW, (x_nome, y_pos), align="left")
            self.score_text(20, f'{int(score):05d}', C_YELLOW, (x_pontos, y_pos), align="left")
            self.score_text(20, f'{date}', C_YELLOW, (x_data, y_pos), align="left")

        self.score_text(16, "ESC - VOLTAR AO MENU", C_WHITE, (WIN_WIDTH / 2, WIN_HEIGHT - 15))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            pygame.display.flip()

    def score_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple, align: str = "center"):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        border_color = (0, 0, 0)

        border_surf: Surface = text_font.render(text, True, border_color).convert_alpha()
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in offsets:
            if align == "left":
                border_rect: Rect = border_surf.get_rect(midleft=(text_pos[0] + dx, text_pos[1] + dy))
            else:
                border_rect: Rect = border_surf.get_rect(center=(text_pos[0] + dx, text_pos[1] + dy))
            self.window.blit(source=border_surf, dest=border_rect)

        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        if align == "left":
            text_rect: Rect = text_surf.get_rect(midleft=text_pos)
        else:
            text_rect: Rect = text_surf.get_rect(center=text_pos)
        self.window.blit(source=text_surf, dest=text_rect)

    def game_over(self):
        pygame.mixer_music.load('./asset/largomix.ogg')
        pygame.mixer_music.play(-1)
        game_over_surf = pygame.image.load('./asset/GameOverBg.png').convert_alpha()
        game_over_rect = game_over_surf.get_rect(left=0, top=0)

        while True:
            self.window.blit(source=game_over_surf, dest=game_over_rect)
            self.score_text(48, 'VOCE PERDEU!!!', C_CYAN, SCORE_POS['Title'])
            self.score_text(20, 'NAVE DESTRUIDA', C_WHITE, SCORE_POS['EnterName'])
            self.score_text(16, 'PRESSIONE ESC OU ENTER PARA VOLTAR AO MENU', C_WHITE, (WIN_WIDTH / 2, WIN_HEIGHT - 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_RETURN:
                        return

def get_formatted_date():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M")
    current_date = current_datetime.strftime("%d/%m/%y")
    return f"{current_time} - {current_date}"
