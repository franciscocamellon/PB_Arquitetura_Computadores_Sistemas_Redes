# -*- coding: utf-8 -*-
"""
/************************ TESTE DE PERFORMANCE 02 **************************
*        Aluno           : Francisco Alves Camello Neto                    *
*        Disciplina      : Projeto de Bloco                                *
*        Professor       : Alcione Santos Dolavale                         *
*        Nome do arquivo : main.py                                         *
***************************************************************************/
"""

import pygame
from src.system import System_Info
from src.components import Elements_Components
# from FRANCISCO_CAMELLO_PB_TP2.src.components import Components


class Info_Screen():
    """ Docstring """

    def __init__(self):
        """ Constructor """
        pygame.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.SCREEN = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.FPS = 60
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAY_NAME = pygame.display.set_caption('Análise do Sistema')
        self.finish = False
        self.count = 60

    def init_game(self):
        """ Docstring """

        while not self.finish:
            # Checar os eventos do mouse aqui:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = True

            if self.count == 60:
                Elements_Components().shows_memory_usage(
                    self.SCREEN, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, System_Info().memory()[4])
                Elements_Components().shows_cpu_usage(
                    self.SCREEN, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, System_Info()._cpu()[2])
                Elements_Components().shows_disk_usage(
                    self.SCREEN, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, System_Info()._disk_usage())

                self.count = 0

            # Atualiza o desenho na tela
            pygame.display.update()

            self.count += 1
            # 60 frames por segundo
            self.FPSCLOCK.tick(self.FPS)
        # Finaliza a janela
        pygame.display.quit()


Info_Screen().init_game()
