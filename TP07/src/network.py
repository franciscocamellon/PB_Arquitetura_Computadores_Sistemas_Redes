# -*- coding: utf-8 -*-
"""
/************************ TESTE DE PERFORMANCE 06 **************************
*        Aluno           : Francisco Alves Camello Neto                    *
*        Disciplina      : Projeto de Bloco                                *
*        Professor       : Alcione Santos Dolavale                         *
*        Nome do arquivo : main.py                                         *
***************************************************************************/
"""

import os
import subprocess
import platform
import errno
import socket
import logging
import pygame


class Network():

    # localhost prefixes
    _local_networks = ("127.", "0:0:0:0:0:0:0:1")

    # ignore these prefixes -- localhost, unspecified, and link-local
    _ignored_networks = _local_networks + ("0.", "0:0:0:0:0:0:0:0", "169.254.", "fe80:")

    def __init__(self):
        pygame.init()
        self.SIZE = (800, 750)
        self.SCREEN = pygame.display.set_mode(
            (self.SIZE[0], self.SIZE[1]))
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (102, 102, 102)
        self.LIGHT_GREY = (230, 230, 230)
        self.FONTSIZE = 16
        self.FONT = pygame.font.SysFont('Arial', self.FONTSIZE)
        self.FPSCLOCK = pygame.time.Clock()
        self.FPS = 60
        self.DISPLAY_NAME = pygame.display.set_caption('Informações de Rede')
        self.finish = False
        self.count = 60
        self.fontIntro = pygame.font.SysFont("Times New Roman", 30)


    def retorna_codigo_ping(self, hostname):
        """Usa o utilitario ping do sistema operacional para encontrar   o host. ('-c 5') indica, em sistemas linux, que deve mandar 5   pacotes. ('-W 3') indica, em sistemas linux, que deve esperar 3   milisegundos por uma resposta. Esta funcao retorna o codigo de   resposta do ping """

        plataforma = platform.system()
        args = []

        if plataforma == "Windows":
            args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]
        else:
            args = ['ping', '-c', '1', '-W', '1', hostname]

        ret_cod = subprocess.call(args,
                                stdout=open(os.devnull, 'w'),
                                stderr=open(os.devnull, 'w'))
        return ret_cod

    def detect_family(self, addr):
        if "." in addr:
            assert ":" not in addr
            return socket.AF_INET
        elif ":" in addr:
            return socket.AF_INET6
        else:
            raise ValueError("invalid ipv4/6 address: %r" % addr)

    def expand_addr(self, addr):
        """convert address into canonical expanded form --
        no leading zeroes in groups, and for ipv6: lowercase hex, no collapsed groups.
        """
        family = self.detect_family(addr)
        addr = socket.inet_ntop(family, socket.inet_pton(family, addr))
        if "::" in addr:
            count = 8-addr.count(":")
            addr = addr.replace("::", (":0" * count) + ":")
            if addr.startswith(":"):
                addr = "0" + addr
        return addr

    def _get_local_addr(self, family, remote):
        try:
            s = socket.socket(family, socket.SOCK_DGRAM)
            try:
                s.connect((remote, 9))
                return s.getsockname()[0]
            finally:
                s.close()
        except socket.error:
            return None

    def get_local_addr(self, remote=None, ipv6=True):
        """get LAN address of host"""
        if remote:
            family = self.detect_family(remote)
            local = self._get_local_addr(family, remote)
            if not local:
                return None
            if family == socket.AF_INET6:
                local = self.expand_addr(local)
            if local.startswith(self._local_networks):
                return local
        else:
            if ipv6:
                local = self._get_local_addr(socket.AF_INET6, "2001:db8::1234")
                if local:
                    local = self.expand_addr(local)
            else:
                local = None
            if not local:
                local = self._get_local_addr(socket.AF_INET, "192.0.2.123")
                if not local:
                    return None
        if local.startswith(self._ignored_networks):
            return None
        return local

    def verifica_hosts(self):
        """Verifica todos os host com a base_ip entre 1 e 255 retorna uma lista com
        todos os host que tiveram resposta 0 (ativo)"""
        disk_surface = pygame.surface.Surface((self.SIZE[0], self.SIZE[1] * 1/3))
        disk_surface.fill(self.LIGHT_GREY)
        text = self.FONT.render("Mapeamento de rede", 1, self.BLACK)
        disk_surface.blit(text, (20, 20))

        local_ip = self.get_local_addr(None, False)
        # print("Mapeando\r")
        host_validos = []
        return_codes = dict()
        for i in range(1, 255):
            host = local_ip + '{0}'.format(i)
            return_codes[host] = self.retorna_codigo_ping(host)

            if i % 20 == 0:
                pygame.draw.rect(disk_surface, self.BLUE,
                            (20, 50, (self.SIZE[0] - 40), 35))
                bar_width = (self.SIZE[0] - 40) * i / 100
                pygame.draw.rect(disk_surface, self.RED,
                                    (20, 50, bar_width, 35))
                self.SCREEN.blit(disk_surface, (0, 0))
            if return_codes[host] == 0:
                host_validos.append(host)
        # print("\nMapping ready...")

        return host_validos
    
    def shows_network_mapping(self, count):
        """ Creates a pygame surface and draws a blue and a red rectangle
        to show cpu usage """
        # host_list = self.verifica_hosts()
        host_list = [0,1,2,3]
        y_pos = 20
        disk_surface = pygame.surface.Surface((self.SIZE[0], self.SIZE[1] * 1/3))
        disk_surface.fill(self.LIGHT_GREY)
        text = self.FONT.render("Mapeamento de rede", 1, self.BLACK)
        disk_surface.blit(text, (20, y_pos))

        for i in range(1, 255):
            pygame.draw.rect(disk_surface, self.BLUE,
                                (20, 50, (self.SIZE[0] - 40), 35))
            bar_width = (self.SIZE[0] - 40) * int(i) / 100
            pygame.draw.rect(disk_surface, self.RED,
                                (20, 50, bar_width, 35))
            # self.SCREEN.blit(disk_surface, (0, 2 * self.SIZE[1] * 2/3))
            self.SCREEN.blit(disk_surface, (0, 0))
        
        
        
        # y_pos += 65

    def init_class(self):
        while not self.finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = True

            # if self.count == 60:
            #     self.shows_network_mapping()
            #     self.count = 0 

            self.verifica_hosts()  
            
            # Atualiza o desenho na tela
            pygame.display.update()

            # self.count += 1
            # 60 frames por segundo
            # self.FPSCLOCK.tick(self.FPS)
        # Finaliza a janela
        pygame.display.quit()

Network().init_class()
# Chamadas
# ip_string = input("Entre com o ip alvo: ")
# ip_lista = ip_string.split('.')
# base_ip = ".".join(ip_lista[0:3]) + '.'
# print("O teste será feito na sub rede: ", base_ip)
# print("Os host válidos são: ", verifica_hosts(base_ip))
