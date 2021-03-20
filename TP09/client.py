# -*- coding: utf-8 -*-
"""
/************************ TESTE DE PERFORMANCE 08 **************************
*        Aluno           : Francisco Alves Camello Neto                    *
*        Disciplina      : Projeto de Bloco                                *
*        Professor       : Alcione Santos Dolavale                         *
*        Nome do arquivo : main.py                                         *
***************************************************************************/
"""

import os
import time
import socket
import psutil
import pickle
from psutil._common import bytes2human

# CLIENT
msgFromClient = " Hello UDP Server"
bytesToSend = msgFromClient.encode('ascii')

serverAddressPort = (socket.gethostname(), 9991)
bufferSize = 4096

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

try:
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    _msg = pickle.loads(msgFromServer[0])

    for k, v in _msg.items():
        if k == "file":
            time.sleep(2)
            print('====' * 23, 'Informações de arquivos e diretótios'.center(92), '====' * 23,
                  '{:<13}{:<30}{:^19}{:^20}{:<10}'.format("Tamanho", "Data de Modificação", "Data de Criação", "Tipo", 'Nome'), sep='\n')
            for _file, _file_values in v.items():
                print('{:<10} {:<27} {:<30} {:<10} {:<15}'.format(
                    _file_values[0], _file_values[1], _file_values[2], _file_values[4], _file))
            print('----' * 23)

        elif k == 'pid':
            time.sleep(2)
            print('====' * 23, 'Informações de processo'.center(92),
                  '====' * 23, sep='\n')
            for pid, info_pid in v.items():
                print('{}{:<10}: {:<30}'.format(' '*2, pid, info_pid))
            print('----' * 23)

        elif k == "cpu":
            time.sleep(2)
            print('====' * 23, 'Informações da CPU'.center(92),
                  '====' * 23, sep='\n')
            for info_type, info in v.items():
                if info_type != 'cpus':
                    print('{}{:<15}: {:<30}'.format(' '*2, info_type, info))
                else:
                    pass
            print('----' * 23)

        elif k == "disk":
            time.sleep(2)
            print('====' * 23, 'Informações do disco'.center(92),
                  '====' * 23, sep='\n')
            templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
            print(templ % ("Device", "Total", "Used", "Free", "Use ", "Type",
                           "Mount"))
            for part in v:
                if os.name == 'nt':
                    if 'cdrom' in part.opts or part.fstype == '':
                        continue
                usage = psutil.disk_usage(part.mountpoint)
                print(templ % (
                    part.device,
                    bytes2human(usage.total),
                    bytes2human(usage.used),
                    bytes2human(usage.free),
                    int(usage.percent),
                    part.fstype,
                    part.mountpoint))
            print('----' * 23)

        elif k == "memory":
            time.sleep(2)
            print('====' * 23, 'Informações de memória'.center(92),
                  '====' * 23, sep='\n')
            for mem, values in v.items():
                for info_type, _info in values.items():
                    print('{}{:<10}: {:<30}'.format(' '*2, info_type, _info))
            print('----' * 23)

        elif k == "scan_host":
            time.sleep(2)
            print('====' * 23, 'Informações de rede'.center(92),
                  '====' * 23, sep='\n')
            for host, host_info in v.items():
                if host == 'hosts':
                    base_ip = host_info[0]
                    base_ip_split = base_ip.split('.')
                    localhost_base_ip = ".".join(base_ip_split[0:3]) + '.'
                    print('{}Hosts válidos na sub-rede: \n\t{}'.format(' '*2, host_info))
                else:
                    print('{}Verificando o host válido: {}'.format(' '*2, host),)
                    if host_info:
                        for i, j in host_info.items():
                        
                            if i == 'Protocolo':
                                print('{}{:<9}: {:<30}'.format(
                                    ' '*4, i, j.upper()))
                            else:
                                for port in j:
                                    print("{}Porta: {:<9} Status: {:<10}".format(
                                        ' '*4, port[0], port[1]))
                    else:
                        print('{}Não há portas!'.format(' '*2))
            print('----' * 23)


except Exception as erro:
    print(str(erro))
