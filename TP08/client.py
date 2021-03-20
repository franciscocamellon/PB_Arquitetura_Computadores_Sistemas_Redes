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
msgFromClient = " Ola servidor UDP!"
bytesToSend = msgFromClient.encode('ascii')

serverAddressPort = (socket.gethostname(), 9991)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

try:
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    _msg = pickle.loads(msgFromServer[0])

    for k, v in _msg.items():
        if k == "cpu":
            print('===' * 25, 'Informações da CPU'.center(75), '===' * 25, sep='\n')
            for info_type, info in v.items():
                if info_type != 'cpus':
                    print('{}: {}'.format(info_type, info))
                else:
                    pass       
            print('---' * 25)
        
        elif k == "disk":
            time.sleep(3)
            print('===' * 25, 'Informações do disco'.center(75), '===' * 25, sep='\n')
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
            print('---' * 25)

        elif k == "memory":
            time.sleep(3)
            print('===' * 25, 'Informações de memória'.center(75), '===' * 25, sep='\n')
            for mem, values in v.items():
                for info_type, _info in values.items():
                    print('{}: {}'.format(info_type, _info))
            print('---' * 25)
            


except Exception as erro:
    print(str(erro))
