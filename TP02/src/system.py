# -*- coding: utf-8 -*-
"""
/************************ TESTE DE PERFORMANCE 02 **************************
*        Aluno           : Francisco Alves Camello Neto                    *
*        Disciplina      : Projeto de Bloco                                *
*        Professor       : Alcione Santos Dolavale                         *
*        Nome do arquivo : main.py                                         *
***************************************************************************/
"""

import psutil
import time
# from validation import Validate


class System_Info():
    """ This function draws squares side by side. """

    def __init__(self):
        """ Constructor. """

        self.mem = psutil.virtual_memory()
        self.cpu_count_phisycal = psutil.cpu_count(logical=False)
        self.cpu_count_logical = psutil.cpu_count(logical=True)
        self.cpu_percent = psutil.cpu_percent(interval=None)
        self.disk_usage = psutil.disk_usage('/')
        self.network = psutil.net_if_addrs()

    def memory(self):
        """ This function receives the input data from users. """

        total = round((self.mem.total)/1024/1024/1024)
        available = round((self.mem.available)/1024/1024/1024)
        used = round((self.mem.used)/1024/1024/1024)
        free = round((self.mem.free)/1024/1024/1024)
        percent = self.mem.percent

        return total, available, used, free, percent

    def _disk_usage(self):
        """ This function receives the input data from users. """
        partitions = []

        for i in psutil.disk_partitions():
            device = i.device
            total = round((psutil.disk_usage(device).total)/1024/1024/1024)
            used = round((psutil.disk_usage(device).used)/1024/1024/1024)
            free = round((psutil.disk_usage(device).free)/1024/1024/1024)
            percent = psutil.disk_usage(i[0]).percent
            partitions.append([device, percent, total, used, free])

        return partitions

    def _cpu(self):
        """ This function process the input data from init_class. """

        total_phisycal = self.cpu_count_phisycal
        total_logical = self.cpu_count_logical
        percent = self.cpu_percent

        return total_phisycal, total_logical, percent

    def _network(self):
        """ This function get the addresses associated to each network
        interface card (NIC) installed on the system and put in a dict
        {NIC: IP}. """
        network = {}
        for k, v in self.network.items():
            if k == 'Loopback Pseudo-Interface 1':
                network[k] = [v[0].address]
            else:
                network[k] = [v[1].address]
        return network


a = System_Info()._network()['Ethernet']
print(a)
