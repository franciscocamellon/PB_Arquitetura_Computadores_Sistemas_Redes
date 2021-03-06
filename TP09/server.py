# -*- coding: utf-8 -*-
"""
/************************ TESTE DE PERFORMANCE 08 **************************
*        Aluno           : Francisco Alves Camello Neto                    *
*        Disciplina      : Projeto de Bloco                                *
*        Professor       : Alcione Santos Dolavale                         *
*        Nome do arquivo : main.py                                         *
***************************************************************************/
"""

import socket
import psutil
import pickle
from system import System_Info as _sys
from network import Network as _net

# SERVER
localIP = socket.gethostname()
localPort = 9991
bufferSize = 1024

msgFromServer = "Olá cliente UDP! Seguem as informações solicitadas:\n"
bytesToSend = str.encode(msgFromServer)

file_directory = _sys()._info_files()
pid_info = _sys()._pid_info()
disk_info = psutil.disk_partitions(all=False)
normal = _sys().memory()[0]
swap = _sys().memory()[1]
cpu = _sys()._cpu_info()
scan_host = _net().verifica_hosts()

message = dict()
message['cpu'] = cpu
message['file'] = file_directory
message['pid'] = pid_info
message['scan_host'] = scan_host
message['memory'] = {'normal':normal}
message['disk'] = disk_info

bytes_to_send = pickle.dumps(message)
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode('ascii')
    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    # Sending a reply to client
    UDPServerSocket.sendto(bytes_to_send, address)
