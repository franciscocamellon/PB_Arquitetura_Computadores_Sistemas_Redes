# -*- coding: utf-8 -*-
"""
/************************ TESTE DE PERFORMANCE 06 **************************
*        Aluno           : Francisco Alves Camello Neto                    *
*        Disciplina      : Projeto de Bloco                                *
*        Professor       : Alcione Santos Dolavale                         *
*        Nome do arquivo : main.py                                         *
***************************************************************************/
"""

import psutil
import time


io_status = psutil.net_io_counters(pernic=True)
nomes = []
for inf in io_status:
    nomes.append(str(inf))


def data_io_mbytes(index):
    """
      Return data usage (sent and received) 
      in MegaBytes.
    """
    rv = io_status[index].bytes_recv / (1024 ** 2)
    st = io_status[index].bytes_sent / (1024 ** 2)
    return rv, st


def data_io_packets(index):
    """
        Return data usage (sent and received) 
        in packets.
    """
    rv = io_status[index].packets_recv
    st = io_status[index].packets_sent
    return rv, st


#MAIN
def main ():
    print("Dados de rede por interface: ")

    for interface in nomes:
        bytes_rv = io_status[interface].bytes_recv
        bytes_st = io_status[interface].bytes_sent
        time.sleep(1)
        vazao_r = io_status[interface].bytes_recv - bytes_rv
        vazao_s = io_status[interface].bytes_sent - bytes_st

        print(interface + ":")
        print("Mbytes recebidos:", round(data_io_mbytes(interface)[0], 2), "MB")
        print("Mbytes enviados:", round(data_io_mbytes(interface)[1], 2), "MB")
        print("Pacotes recebidos:", data_io_packets(interface)[0])
        print("Pacotes enviados:", data_io_packets(interface)[1])
        print("Vazão em bytes recebidos:", vazao_r)
        print("Vazao em bytes enviados:", vazao_s)
        print("\n" + "-" * 25)
    print("\n" + "-" * 35)


main()