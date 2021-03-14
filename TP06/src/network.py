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
    _ignored_networks = _local_networks + \
        ("0.", "0:0:0:0:0:0:0:0", "169.254.", "fe80:")

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
        self.DISPLAY_NAME = pygame.display.set_caption('Mapeando informações de Rede')
        self.finish = False
        self.count = 60
        self.fontIntro = pygame.font.SysFont("Times New Roman", 30)
        self.valid_hosts = []
        self.localhost = ''
        self.localhost_base_ip = ''

    def get_local_addr(self, remote=None, ipv6=True):
        """get LAN address of localhost"""

        def detect_family(addr):
            if "." in addr:
                assert ":" not in addr
                return socket.AF_INET
            elif ":" in addr:
                return socket.AF_INET6
            else:
                raise ValueError("invalid ipv4/6 address: %r" % addr)

        def expand_addr(addr):
            """convert address into canonical expanded form --
            no leading zeroes in groups, and for ipv6: lowercase hex, no collapsed groups.
            """
            family = detect_family(addr)
            addr = socket.inet_ntop(family, socket.inet_pton(family, addr))
            if "::" in addr:
                count = 8-addr.count(":")
                addr = addr.replace("::", (":0" * count) + ":")
                if addr.startswith(":"):
                    addr = "0" + addr
            return addr

        def _get_local_addr(family, remote):
            try:
                s = socket.socket(family, socket.SOCK_DGRAM)
                try:
                    s.connect((remote, 9))
                    return s.getsockname()[0]
                finally:
                    s.close()
            except socket.error:
                return None

        if remote:
            family = detect_family(remote)
            local = _get_local_addr(family, remote)
            if not local:
                return None
            if family == socket.AF_INET6:
                local = expand_addr(local)
            if local.startswith(self._local_networks):
                return local
        else:
            if ipv6:
                local = _get_local_addr(socket.AF_INET6, "2001:db8::1234")
                if local:
                    local = expand_addr(local)
            else:
                local = None
            if not local:
                local = _get_local_addr(socket.AF_INET, "192.0.2.123")
                if not local:
                    return None
        if local.startswith(self._ignored_networks):
            return None
        return local

    def verifica_hosts(self):
        """Verifica todos os host com a base_ip entre 1 e 255 retorna uma lista com
        todos os host que tiveram resposta 0 (ativo)"""

        def retorna_codigo_ping(hostname):
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

        localhost_ip = self.get_local_addr(None, False)
        self.localhost = localhost_ip
        localhost_ip_split = localhost_ip.split('.')
        localhost_base_ip = ".".join(localhost_ip_split[0:3]) + '.'
        self.localhost_base_ip = localhost_base_ip
        print("Mapeando\r")
        return_codes = dict()
        for i in range(1, 255):
            host = localhost_base_ip + '{0}'.format(i)
            return_codes[host] = retorna_codigo_ping(host)

            if i % 20 == 0:
                print('.')
            if return_codes[host] == 0:
                self.valid_hosts.append(host)
        print("\nMapping ready...")
        return self.valid_hosts

    def show_network_text(self):
        text_surface = pygame.surface.Surface((self.SIZE[0], self.SIZE[1]))
        text_surface.fill(self.LIGHT_GREY)
        title = self.FONT.render("O teste foi feito na sub rede: {}".format(
            self.localhost_base_ip), True, self.BLACK)
        text_surface.blit(title, (20, 20))
        line_spacing = title.get_height() + 20
        sub_title = self.FONT.render("Os host válidos são: ", True, self.BLACK)
        text_surface.blit(sub_title, (30, line_spacing))
        line_spacing += 20

        for host in self.valid_hosts:
            host_text = self.FONT.render(host, True, self.BLACK)
            text_surface.blit(host_text, (35, line_spacing))
            line_spacing += 20
        self.SCREEN.blit(text_surface, (0, 0))

        # y_pos += 65

    def init_class(self):

        self.verifica_hosts()
        self.DISPLAY_NAME = pygame.display.set_caption('Informações de Rede')

        while not self.finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = True

            # if self.count == 60:
            #     self.shows_network_mapping()
            #     self.count = 0

            
            self.show_network_text()

            # Atualiza o desenho na tela
            pygame.display.update()

            # self.count += 1
            # 60 frames por segundo
            # self.FPSCLOCK.tick(self.FPS)
        # Finaliza a janela
        pygame.display.quit()


Network().init_class()
