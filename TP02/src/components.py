# -*- coding: utf-8 -*-
"""
/************************ TESTE DE PERFORMANCE 02 **************************
*        Aluno           : Francisco Alves Camello Neto                    *
*        Disciplina      : Projeto de Bloco                                *
*        Professor       : Alcione Santos Dolavale                         *
*        Nome do arquivo : main.py                                         *
***************************************************************************/
"""

import psutil
import pygame


class Elements_Components():
    """ Docstring """

    def __init__(self):
        """ Constructor """
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.FONTSIZE = 30
        self.FONT = pygame.font.SysFont(None, self.FONTSIZE)

    def shows_memory_usage(self, screen, width, height, memory):
        """ Creates a pygame surface and draws a blue and a red rectangle
        to show memory usage """

        memory_surface = pygame.surface.Surface((width, height // 3))
        pygame.draw.rect(memory_surface, self.BLUE,
                         (20, 50, (width - 2 * 20), 70))
        bar_width = (width - 2 * 20) * memory / 100
        pygame.draw.rect(memory_surface, self.RED, (20, 50, bar_width, 70))
        screen.blit(memory_surface, (0, 0))
        bar_text = 'Uso de Memória (Em uso: {}%):'.format(memory)
        text = self.FONT.render(bar_text, 1, self.WHITE)
        screen.blit(text, (20, 20))

    def shows_cpu_usage(self, screen, width, height, cpu):
        """ Creates a pygame surface and draws a blue and a red rectangle
        to show cpu usage """

        cpu_surface = pygame.surface.Surface((width, height // 3))
        pygame.draw.rect(cpu_surface, self.BLUE, (20, 50, (width - 2 * 20), 70))
        bar_width = (width - 2 * 20) * cpu / 100
        pygame.draw.rect(cpu_surface, self.RED, (20, 50, bar_width, 70))
        screen.blit(cpu_surface, (0, height // 3))
        bar_text = 'Uso da CPU (Em uso: {}%):'.format(cpu)
        text = self.FONT.render(bar_text, 1, self.WHITE)
        screen.blit(text, (20, (height // 3) + 20))

    def shows_disk_usage(self, screen, width, height, disk):
        """ Creates a pygame surface and draws a blue and a red rectangle
        to show cpu usage """
        """
        y_pos = 16

        if isinstance(disk[0], list):
            # disk_surface = pygame.surface.Surface((width, height))
            disk_surface = pygame.surface.Surface((width, height // 3))
            for device in disk:
                pygame.draw.rect(disk_surface, self.BLUE, (20, y_pos, (width - 2 * 20), 35))
                bar_width = (width - 2 * 20) * device[1] / 100
                pygame.draw.rect(disk_surface, self.RED, (20, y_pos, bar_width, 35))
                screen.blit(disk_surface, (0, 2 * height // 3))
                bar_text = 'Disco {} (Em uso: {}%):'.format(device[0], device[1])
                text = self.FONT.render(bar_text, 1, self.WHITE)
                disk_surface.blit(text, (20, y_pos))
                y_pos += 65

            # for device in disk:
            #     pygame.draw.rect(disk_surface, self.BLUE, (20, y_pos, (width - 2 * 20), 35))
            #     bar_width = (width - 2 * 20) * device[1] / 100
            #     pygame.draw.rect(disk_surface, self.RED, (20, y_pos, bar_width, 35))
            #     screen.blit(disk_surface, (0, 0))
            #     bar_text = 'Disco {} (Em uso: {}%):'.format(device[0], device[1])
            #     text = self.FONT.render(bar_text, 1, self.WHITE)
            #     screen.blit(text, (20, y_pos + 20) )
            #     y_pos += 65
        else:
        """
        disk_surface = pygame.surface.Surface((width, height // 3))
        pygame.draw.rect(disk_surface, self.BLUE, (20, 50, (width - 2 * 20), 70))
        bar_width = (width - 2 * 20) * disk[0][1] / 100
        pygame.draw.rect(disk_surface, self.RED, (20, 50, bar_width, 70))
        screen.blit(disk_surface, (0, 2 * height // 3))
        bar_text = 'Disco {} (Em uso: {}%):'.format(disk[0][0], disk[0][1])
        text = self.FONT.render(bar_text, 1, self.WHITE)
        screen.blit(text, (20, (2 * height // 3) + 20))