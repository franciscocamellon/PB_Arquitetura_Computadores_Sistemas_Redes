# -*- coding: utf-8 -*-
'''
/************************ TESTE DE PERFORMANCE 03 **************************
*        Aluno           : Francisco Alves Camello Neto                    *
*        Disciplina      : Projeto de Bloco                                *
*        Professor       : Alcione Santos Dolavale                         *
*        Nome do arquivo : main.py                                         *
***************************************************************************/
'''

import os
import cpuinfo
import psutil
import subprocess
import sched
import threading
import time
from psutil._common import bytes2human


class System_Info():
    ''' This class retrieves some types of system information. '''

    def __init__(self):
        ''' Constructor. '''
        self.cpu_info = cpuinfo.get_cpu_info()
        self.cpu_count_phisycal = psutil.cpu_count(logical=False)
        self.cpu_count_logical = psutil.cpu_count(logical=True)
        self.cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
        self.disk_usage = psutil.disk_usage('/')
        self.network = psutil.net_if_addrs()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        

    def memory(self):
        ''' This function returns a dict of memory informations. '''
        def format_info(info):
            dict_info = dict()
            for name in info._fields:
                value = getattr(info, name)
                if name != 'percent':
                    value = bytes2human(value)
                dict_info[name.capitalize()] = value
            return dict_info

        memory = format_info(psutil.virtual_memory())
        swap = format_info(psutil.swap_memory())
        return memory, swap

    def _disk_usage(self):
        ''' This function returns a dict of disk partitions and your usages. '''
        usage_dict = dict()
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    continue
            usage = psutil.disk_usage(part.mountpoint)
            usage_dict[part.device] = [bytes2human(usage.total),
                                       bytes2human(usage.used),
                                       bytes2human(usage.free),
                                       int(usage.percent),
                                       part.fstype,
                                       part.mountpoint]
        return usage_dict

    def _cpu_info(self):
        ''' This function returns a dictionary with informations about the cpu. '''
        cpu_dict = dict()
        cpu_dict['Name: '] = self.cpu_info['brand_raw']
        cpu_dict['Architecture: '] = self.cpu_info['arch']
        cpu_dict['Bits: '] = self.cpu_info['bits']
        if self.cpu_info['hz_actual'][0] % 10**9 > 0:
            cpu_dict['Frequency: '] = str(
                round((self.cpu_info['hz_actual'][0]/10**9), 2)) + ' Ghz'
        elif self.cpu_info['hz_actual'][0] % 10**6 > 0:
            cpu_dict['Frequency: '] = str(
                round((self.cpu_info['hz_actual'][0]/10**9), 2)) + ' Mhz'
        elif self.cpu_info['hz_actual'][0] % 10**3 > 0:
            cpu_dict['Frequency: '] = str(
                round((self.cpu_info['hz_actual'][0]/10**9), 2)) + ' Khz'
        cpu_dict['Physical Cores: '] = self.cpu_count_phisycal
        cpu_dict['Logical Cores: '] = self.cpu_count_logical
        cpu_dict['cpus'] = self.cpu_percent
        return cpu_dict

    def _network(self):
        ''' This function get the addresses associated to each network
        interface card (NIC) installed on the system and put in a dict
        {NIC: IP}. '''
        network = {}
        for k, v in self.network.items():
            if k == 'Loopback Pseudo-Interface 1':
                network[k] = [v[0].address]
            else:
                network[k] = [v[1].address]
        return network

    def _directory_file_info(self, text=None):
        print ('INICIO DO EVENTO:', time.ctime(), text)
        path = ".\\"
        os.chdir(path)
        current_path = os.getcwd()
        dir_list = os.listdir(current_path)
        info_dict = dict()

        if text == 'arquivo':
            for i in dir_list:
                if os.path.isfile(i):
                    ext = os.path.splitext(i)[1]
                    if not ext in info_dict:
                        info_dict[ext] = dict()
                    info_dict[ext][i] = [bytes2human(os.stat(i).st_size),
                                        time.ctime(os.stat(i).st_mtime),
                                        time.ctime(os.stat(i).st_atime)
                                        ]
                else:
                    pass
        else:
            for i in dir_list:
                if not os.path.isfile(i):
                    if not i in info_dict:
                        info_dict[i] = list()
                    info_dict[i] = [bytes2human(os.stat(i).st_size),
                                        time.ctime(os.stat(i).st_atime),
                                        time.ctime(os.stat(i).st_mtime)
                                        ]
                else:
                    pass

        return info_dict

    def _directory_info(self, text=None):
        print ('INICIO DO EVENTO:', time.ctime(), text)
        path = ".\\"
        os.chdir(path)
        current_path = os.getcwd()
        dir_list = os.listdir(current_path)
        directory_dict = dict()

        for i in dir_list:
            if not os.path.isfile(i):
                if not i in directory_dict:
                    directory_dict[i] = list()
                directory_dict[i] = [bytes2human(os.stat(i).st_size),
                                     time.ctime(os.stat(i).st_atime),
                                     time.ctime(os.stat(i).st_mtime)
                                     ]
            else:
                pass

        for _file, _file_values in directory_dict.items():
            print('  {:<10} {:<27} {:<30} {:<10}'.format(_file_values[0], _file_values[1], _file_values[2], _file))
        print ('FIM DO EVENTO:', time.ctime(), text)
        
        return directory_dict

    def _pid_info(self, text=None):
        print ('INICIO DO EVENTO:', time.ctime(), text)
        name = 'python.exe'
        lp = psutil.pids()
        info_dict = dict()
        for i in lp:
            try:
                p = psutil.Process(i)
                exec_path = p.exe()
                if psutil.pid_exists(i) and p.name() == name:
                    info_dict['Executável'] = exec_path.split('\\')[-1]
                    info_dict['PID'] = i
                    info_dict['Threads'] = p.num_threads()
                    info_dict['Criação'] = time.ctime(p.create_time())
                    info_dict['T. Usu.'] = p.cpu_times().user
                    info_dict['T. Sis.'] = p.cpu_times().system
                    info_dict['Mem. (%)'] = round(p.memory_percent(),2)
                    info_dict['RSS'] = bytes2human(p.memory_info().rss)
                    info_dict['VMS'] = bytes2human(p.memory_info().vms)
            except:
                pass
        for pid, info_pid in info_dict.items():
            print('{}{:<10}: {:<30}'.format(' '*2, pid, info_pid))

        print ('FIM DO EVENTO:', time.ctime(), text)
        return info_dict

    def _scheduler(self):

        print ('INICIO:', time.ctime())
        self.scheduler.enter(5, 1, self._pid_info, ('_file_info()',))
        self.scheduler.enter(3, 1, self._directory_info, ('_directory_info()',))
        print ('CHAMADAS ESCALONADAS DA FUNÇÃO:', time.ctime())

        self.scheduler.run()

System_Info()._scheduler()
