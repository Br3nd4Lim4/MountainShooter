import random
import sys
import pygame
from pygame import Surface
from code.Const import (
    C_WHITE,
    MENU_OPTION,
    EVENT_ENEMY,
    SPAWN_TIME,
    C_GREEN,
    C_CYAN,
    EVENT_TIMEOUT,
    TIMEOUT_STEP,
    TIMEOUT_LEVEL)
from code.Enemy import Enemy
from code.Boss import Boss
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:

    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.timeout = TIMEOUT_LEVEL
        self.boss_spawned = False
        self.boss_defeated = False
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(
            EntityFactory.get_entity(self.name + 'Bg'))
        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]
        self.entity_list.append(player)

        if game_mode in [
            MENU_OPTION[1],
            MENU_OPTION[2]]:
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]
            self.entity_list.append(player)

        if self.name == 'Level2':
            boss = EntityFactory.get_entity('Boss')
            self.entity_list.append(boss)
            self.boss_spawned = True

        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)

    def update_player_score(self, player_score):
        for ent in self.entity_list:
            if ent.name == 'Player1':
                player_score[0] = ent.score
            elif ent.name == 'Player2':
                player_score[1] = ent.score

    def run(self, _player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.set_volume(0.3)
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
                if isinstance(ent, (Player, Enemy, Boss)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

                if ent.name == 'Player1':
                    Level.level_text(self.window, 14, f'JOGADOR 1 - VIDA: {ent.health} | PONTUACAO: {ent.score}',
                                     C_GREEN, (10, 25))
                if ent.name == 'Player2':
                    Level.level_text(self.window, 14, f'JOGADOR 2 - VIDA: {ent.health} | PONTUACAO: {ent.score}',
                                     C_CYAN, (10, 45))

            if self.name == 'Level2':
                boss_ent = next((ent for ent in self.entity_list if isinstance(ent, Boss)), None)
                if boss_ent:
                    Level.level_text(self.window, 14, f'VIDA DO BOSS: {boss_ent.health}', C_WHITE, (10, 5))
            elif self.name == 'Level1':
                Level.level_text(self.window, 14, f'{self.name} - TEMPO: {self.timeout / 1000:.1f}s', C_WHITE, (10, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY and self.name == 'Level1':
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))
                if event.type == EVENT_TIMEOUT and self.name == 'Level1':
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout <= 0:
                        self.update_player_score(_player_score)
                        return True

            pygame.display.flip()
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

            if self.name == 'Level2':
                boss_ent = next((ent for ent in self.entity_list if isinstance(ent, Boss)), None)
                if boss_ent is None:
                    self.boss_defeated = True

                if self.boss_defeated:
                    self.update_player_score(_player_score)
                    return True

            if not any(isinstance(ent, Player) for ent in self.entity_list):
                return False

    @staticmethod
    def level_text(
            window: Surface,
            text_size: int,
            text: str,
            text_color: tuple,
            text_pos: tuple):

        text_font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        window.blit(source=text_surf, dest=text_rect)
