# -*- coding: utf-8 -*-
"""
/************************ TESTE DE PERFORMANCE 06 **************************
*        Aluno           : Francisco Alves Camello Neto                    *
*        Disciplina      : Projeto de Bloco                                *
*        Professor       : Alcione Santos Dolavale                         *
*        Nome do arquivo : main.py                                         *
***************************************************************************/
"""

import socket
import os


def ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


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


def main():
    print("Dados da rede: ")
    print("{}IP:".format(' '*3), ip())
    default_gateways = default_gateway()
    subnet_masks = subnet_mask()
    print("\n" + "-" * 35)

main()