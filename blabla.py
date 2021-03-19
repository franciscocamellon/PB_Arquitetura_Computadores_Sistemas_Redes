import psutil, time
def _pid_info():
    name = 'python.exe'
    lp = psutil.pids()
    pid_list = []
    info_dict = dict()
    for i in lp:
        p = psutil.Process(i)
        if p.name() == name:
            info_dict['PID'] = i
            info_dict['Threads'] = p.num_threads()
            info_dict['PID'] = time.ctime(p.create_time())
            info_dict['PID'] = p.cpu_times().user
            info_dict['PID'] = p.cpu_times().system
            info_dict['PID'] = p.memory_percent() + " MB"
            info_dict['PID'] = (p.memory_info().rss)/1024/1024 + " MB"
            info_dict['PID'] = (p.memory_info().vms)/1024/1024 + " MB"
            info_dict['PID'] = p.exe()
            pid_list.append(i)
            pid_list.append()
    return pid_list

print(_pid_info())