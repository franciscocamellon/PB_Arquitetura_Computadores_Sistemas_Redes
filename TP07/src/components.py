# -*- coding: utf-8 -*-
"""
/************************ TESTE DE PERFORMANCE 06 **************************
*        Aluno           : Francisco Alves Camello Neto                    *
*        Disciplina      : Projeto de Bloco                                *
*        Professor       : Alcione Santos Dolavale                         *
*        Nome do arquivo : main.py                                         *
***************************************************************************/
"""

import pygame
import cpuinfo
import psutil
import time


class Elements_Components():
    """ Docstring  """

    def __init__(self):
        """ Constructor """
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (102, 102, 102)
        self.LIGHT_GREY = (230, 230, 230)
        self.FONTSIZE = 16
        self.FONT = pygame.font.SysFont('Arial', self.FONTSIZE)

    def shows_memory_usage(self, screen, width, height, memory):
        """ Creates a pygame surface and draws a blue and a red rectangle
        to show memory usage """

        memory_surface = pygame.surface.Surface((width, height * 2/4))
        memory_surface.fill(self.GREY)
        pygame.draw.rect(memory_surface, self.BLUE,
                         (20, 50, (width - 2 * 20), 70))
        bar_width = (width - 2 * 20) * \
            int(round(float(memory['Total'][:-1])))/100
        pygame.draw.rect(memory_surface, self.RED, (20, 50, bar_width, 70))
        screen.blit(memory_surface, (0, height * 2/4))
        bar_text = 'Uso de Memória (Em uso: {}%):'.format(memory['Percent'])
        text = self.FONT.render(bar_text, 1, self.WHITE)
        screen.blit(text, (20, height * 2/4 + 20))

    def shows_memory_text(self, screen, width, height, _dict, pos_y, text, pos):
        text_surface = pygame.surface.Surface((width, height * 1/4))
        text_surface.fill(self.LIGHT_GREY)
        title = self.FONT.render(text, True, self.BLACK)
        text_surface.blit(title, (20, pos_y))
        line_spacing = 23
        for k, v in _dict.items():
            text = self.FONT.render(str(k)+':', True, self.BLACK)
            text_surface.blit(text, (20, pos_y + line_spacing))
            text2 = self.FONT.render(str(v), True, self.BLACK)
            text_surface.blit(text2, (170, pos_y + line_spacing))
            line_spacing += 23
        screen.blit(text_surface, pos)

    def show_cpu_usage(self, screen, width, height, cpu_percent):
        surface = pygame.surface.Surface((width, height))
        surface.fill(self.GREY)
        x = y = desl = 10

        column_height = height * 4/5 - 2 * 10
        column_width = (
            width - 2 * 10 - (len(cpu_percent['cpus']) + 1) * 10) / len(cpu_percent['cpus'])

        d = x + desl

        for i in cpu_percent['cpus']:

            pygame.draw.rect(surface, self.RED,
                             (d, y, column_width, column_height))
            pygame.draw.rect(surface, self.BLUE,
                             (d, y, column_width, (1-i/100)*column_height))
            d = d + column_width + desl

        screen.blit(surface, (0, height / 5))

    def show_cpu_text(self, screen, width, height, _dict, pos_y):
        text_surface = pygame.surface.Surface((width, height * 1/5))
        text_surface.fill(self.LIGHT_GREY)

        line_spacing = 0
        # line_size = text.get_width()
        for k, v in _dict.items():
            if k == 'cpus':
                pass
            else:
                text = self.FONT.render(str(k), True, self.BLACK)
                text_surface.blit(text, (20, pos_y + line_spacing))
                text2 = self.FONT.render(str(v), True, self.BLACK)
                text_surface.blit(text2, (170, pos_y + line_spacing))
                line_spacing += 23
        screen.blit(text_surface, (0, 0))

    def show_network_text(self, screen, width, height, network, pos_y):
        text_surface = pygame.surface.Surface((width, height))
        text_surface.fill(self.LIGHT_GREY)

        line_spacing = 0

        for k, v in network.items():
            text = self.FONT.render(str(k) + ': ', True, self.BLACK)
            line_size = text.get_width()
            text_surface.blit(text, (20, pos_y + line_spacing))
            text2 = self.FONT.render(str(v[0]), True, self.GREY)
            text_surface.blit(text2, (line_size + 20, pos_y + line_spacing))
            line_spacing += 23
        screen.blit(text_surface, (0, 0))

    def shows_disk_usage(self, screen, width, height, disk):
        """ Creates a pygame surface and draws a blue and a red rectangle
        to show cpu usage """

        y_pos = 16
        disk_surface = pygame.surface.Surface((width, height * 2/3))
        disk_surface.fill(self.GREY)

        for device, values in disk.items():
            pygame.draw.rect(disk_surface, self.BLUE,
                             (20, y_pos, (width - 2 * 20), 35))
            bar_width = (width - 2 * 20) * int(float(values[0][:-1])) / 100
            pygame.draw.rect(disk_surface, self.RED,
                             (20, y_pos, bar_width, 35))
            screen.blit(disk_surface, (0, 2 * height * 2/3))
            bar_text = 'Disco {} (Em uso: {}%):'.format(device, values[3])
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
        """else:

        disk_surface = pygame.surface.Surface((width, height // 3))
        pygame.draw.rect(disk_surface, self.BLUE,
                         (20, 50, (width - 2 * 20), 70))
        bar_width = (width - 2 * 20) * disk[0][1] / 100
        pygame.draw.rect(disk_surface, self.RED, (20, 50, bar_width, 70))
        screen.blit(disk_surface, (0, 2 * height // 3))
        bar_text = 'Disco {} (Em uso: {}%):'.format(disk[0][0], disk[0][1])
        text = self.FONT.render(bar_text, 1, self.WHITE)
        screen.blit(text, (20, (2 * height // 3) + 20))"""

    def shows_disk_text(self, screen, width, height, _dict, pos_y):
        text_surface = pygame.surface.Surface((width, height * 1/3))
        text_surface.fill(self.LIGHT_GREY)
        templ = "%-15s %8s %9s %10s %8s%% %9s  %s"
        text = self.FONT.render(templ % ("Device", "Total", "Used", "Free", "Use ", "Type",
                                         "Mount"), True, self.BLACK)
        text_surface.blit(text, (20, pos_y))
        line_spacing = 23
        for k, v in _dict.items():
            text = self.FONT.render(
                templ % (k, v[0], v[1], v[2], v[3], v[4], v[5]),
                True,
                self.BLACK)
            text_surface.blit(text, (20, pos_y + line_spacing))
            line_spacing += 23
        screen.blit(text_surface, (0, 0))

    def shows_info_file_text(self, screen, width, height, _dict, pos_y):
        text_surface = pygame.surface.Surface((width, height))
        text_surface.fill(self.LIGHT_GREY)
        title = 'Informações sobre arquivos e diretórios'
        subtitle = '{:<11}'.format("Tamanho") + '{:^30}'.format("Data de Modificação") + \
            '{:^35}'.format("Data de Criação") + \
            '{:^11}'.format("Tipo") + 'Nome'.rjust(15)
        text = self.FONT.render(title, True, self.BLACK)
        text2 = self.FONT.render(subtitle, True, self.BLACK)
        text_surface.blit(text, (20, pos_y))

        text_surface.blit(text2, (20, 35))
        line_spacing = 58

        for k, v in _dict.items():
            text = self.FONT.render(
                '{:<15} {:<27} {:<30} {:^11} {:<15}'.format(
                    v[0], v[1], v[2], v[4], k),
                True,
                self.BLACK)
            text_surface.blit(text, (20, pos_y + line_spacing))
            line_spacing += 23
        screen.blit(text_surface, (0, 0))

    def shows_pid_info_text(self, screen, width, height, pid_list, pos_y):
        text_surface = pygame.surface.Surface((width, height))
        text_surface.fill(self.LIGHT_GREY)
        titulo = '{:^7}'.format("PID")
        titulo = titulo + '{:^11}'.format("# Threads")
        titulo = titulo + '{:^26}'.format("Criação")
        titulo = titulo + '{:^9}'.format("T. Usu.")
        titulo = titulo + '{:^9}'.format("T. Sis.")
        titulo = titulo + '{:^12}'.format("Mem. (%)")
        titulo = titulo + '{:^12}'.format("RSS")
        titulo = titulo + '{:^12}'.format("VMS")
        titulo = titulo + " Executável"
        text = self.FONT.render(
            titulo,
            True,
            self.BLACK)
        text_surface.blit(text, (20, pos_y))
        line_spacing = 23
        if len(pid_list) > 0:
            for pid in pid_list:
                try:
                    p = psutil.Process(pid)
                    texto = '{:6}'.format(pid)
                    texto = texto + '{:11}'.format(p.num_threads())
                    texto = texto + " " + time.ctime(p.create_time()) + " "
                    texto = texto + '{:8.2f}'.format(p.cpu_times().user)
                    texto = texto + '{:8.2f}'.format(p.cpu_times().system)
                    texto = texto + \
                        '{:10.2f}'.format(p.memory_percent()) + " MB"
                    rss = (p.memory_info().rss)/1024/1024
                    texto = texto + '{:10.2f}'.format(rss) + " MB"
                    vms = p.memory_info().vms/1024/1024
                    texto = texto + '{:10.2f}'.format(vms) + " MB"
                    texto = texto + " " + p.exe()
                    # return texto
                    text = self.FONT.render(
                        texto,
                        True,
                        self.BLACK)
                    text_surface.blit(text, (20, pos_y + line_spacing))
                    line_spacing += 23
                except:
                    pass
                break

        screen.blit(text_surface, (0, 0))
