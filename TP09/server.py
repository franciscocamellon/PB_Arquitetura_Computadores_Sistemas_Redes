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

# SERVER
localIP = socket.gethostname()
localPort = 9991
bufferSize = 1024

msgFromServer = "Olá cliente UDP"
bytesToSend = str.encode(msgFromServer)

disk_info = psutil.disk_partitions(all=False)
normal = _sys().memory()[0]
swap = _sys().memory()[1]
cpu = _sys()._cpu_info()
message = dict()
message['cpu'] = cpu
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
