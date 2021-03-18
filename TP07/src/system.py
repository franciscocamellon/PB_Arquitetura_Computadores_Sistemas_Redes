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

net_counters = psutil.net_io_counters()

def data_io_mbytes():
    """
        Return data usage (sent and received) 
        in MegaBytes.
    """
    rv = net_counters.bytes_recv / (1024 ** 2)
    st = net_counters.bytes_sent / (1024 ** 2)
    return rv, st


def data_io_packets():
    """
        Return data usage (sent and received) 
        in packets.
    """
    rv = net_counters.packets_recv
    st = net_counters.packets_sent
    return rv, st


#MAIN
def main ():
    print("Dados de rede por processos: ")
    bytes_rv = net_counters.bytes_recv
    bytes_st = net_counters.bytes_sent
    time.sleep(1)
    vazao_r = net_counters.bytes_recv - bytes_rv
    vazao_s = net_counters.bytes_sent - bytes_st

    print("Mbytes recebidos:", round(data_io_mbytes()[0], 2), "MB")
    print("Mbytes enviados:", round(data_io_mbytes()[1], 2), "MB")
    print("Pacotes recebidos:", data_io_packets()[0])
    print("Pacotes enviados:", data_io_packets()[1],"\n")
    print("Vazão em bytes recebidos:", vazao_r)
    print("Vazao em bytes enviados:", vazao_s)
    print("\n" + "-" * 35)

main()