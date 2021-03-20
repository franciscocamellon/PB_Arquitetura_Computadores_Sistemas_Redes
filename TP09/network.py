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
import nmap


class Network():

    nmScan = nmap.PortScanner()

    # localhost prefixes
    _local_networks = ("127.", "0:0:0:0:0:0:0:1")

    # ignore these prefixes -- localhost, unspecified, and link-local
    _ignored_networks = _local_networks + \
        ("0.", "0:0:0:0:0:0:0:0", "169.254.", "fe80:")

    def __init__(self):
        self.valid_hosts = dict()
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

        def scan_host(host):
            self.nmScan.scan(host)
            for proto in self.nmScan[host].all_protocols():
                lport = self.nmScan[host][proto].keys()
                result = dict()
                result['Protocolo'] = proto
                result['Portas'] = list()
                for port in lport:
                    result['Portas'].append((port, self.nmScan[host][proto][port]['state']))
                # net_scan = dict()
                # net_scan[host] = result
                return result

        def default_gateway():
            if os.name == "posix":
                dgw = os.system('ip r | grep default | awk {"print $3"}')
                return dgw
            if os.name == "nt":
                dgw = os.system('ipconfig | findstr /i "Gateway"')
                return dgw


        def subnet_mask():
            if os.name == "posix":
                sm = os.system('ip r | grep default | awk {"print $3"}')
                return sm
            if os.name == "nt":
                sm = os.system('ipconfig | findstr /i "Sub-rede"')
                return sm


        localhost_ip = self.get_local_addr(None, False)
        self.localhost = localhost_ip
        localhost_ip_split = localhost_ip.split('.')
        localhost_base_ip = ".".join(localhost_ip_split[0:3]) + '.'
        self.localhost_base_ip = localhost_base_ip
        print("Mapeando\r")
        return_codes = dict()
        valid_hosts = []
        self.valid_hosts['hosts'] = []
        for i in range(1, 255):
            host = localhost_base_ip + '{0}'.format(i)
            return_codes[host] = retorna_codigo_ping(host)

            if i % 20 == 0:
                print('.')
            
            if return_codes[host] == 0:
                valid_hosts.append(host)
                self.valid_hosts['hosts'].append(host)
                self.valid_hosts[host] = scan_host(host)

        print("\nMapping ready...")

        return self.valid_hosts

    