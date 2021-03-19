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


class MainWindow():
    """ Docstring """

    def __init__(self):
        pygame.init()
        self.SIZE = (800, 750)
        self.SCREEN = pygame.display.set_mode(
            (self.SIZE[0], self.SIZE[1]))
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAY_NAME = pygame.display.set_caption('Análise do Sistema')
        self.finish = False
        self.FPS_COUNT = 60
        self.count = 5
        self.fontIntro = pygame.font.SysFont("Times New Roman", 30)

    def drawIntro(self, screen):

        if self.count == 0:
            Elements_Components().show_cpu_text(
                screen,
                self.SIZE[0],
                self.SIZE[1],
                System_Info()._cpu_info(), 5)
            Elements_Components().show_cpu_usage(
                screen,
                self.SIZE[0],
                self.SIZE[1],
                System_Info()._cpu_info())

        elif self.count == 1:
            Elements_Components().shows_memory_text(
                screen,
                self.SIZE[0],
                self.SIZE[1],
                System_Info().memory()[0], 5, 'Memory', (0, 0))

            Elements_Components().shows_memory_text(
                screen,
                self.SIZE[0],
                self.SIZE[1],
                System_Info().memory()[1], 5, 'Swap', (0, self.SIZE[1]*1/4))
            Elements_Components().shows_memory_usage(
                screen,
                self.SIZE[0],
                self.SIZE[1],
                System_Info().memory()[0])

        elif self.count == 2:
            Elements_Components().shows_disk_usage(
                screen,
                self.SIZE[0],
                self.SIZE[1],
                System_Info()._disk_usage())

            Elements_Components().shows_disk_text(
                screen,
                self.SIZE[0],
                self.SIZE[1],
                System_Info()._disk_usage(), 5)

        elif self.count == 3:
            Elements_Components().show_network_text(
                screen,
                self.SIZE[0],
                self.SIZE[1],
                System_Info()._network(), 10)

        elif self.count == 4:
            pass
            Elements_Components().shows_info_file_text(
                screen,
                self.SIZE[0],
                self.SIZE[1],
                System_Info()._directory_file_info(), 10, 'arquivos')
            Elements_Components().shows_info_file_text(
                screen,
                self.SIZE[0],
                self.SIZE[1],
                System_Info()._directory_file_info(), 100, 'Diretórios')
                
        elif self.count == 5:
            Elements_Components().shows_pid_info_text(
                screen,
                self.SIZE[0],
                self.SIZE[1],
                System_Info()._pid_info(), 10)

    def init_class(self):
        while not self.finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.count += 1
                    elif event.key == pygame.K_LEFT:
                        self.count -= 1

            self.drawIntro(self.SCREEN)
            pygame.display.flip()

        pygame.quit()


MainWindow().init_class()
