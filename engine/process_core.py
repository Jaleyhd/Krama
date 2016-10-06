from multiprocessing import Process
import subprocess
from ..conf import common



def multiprocess_parallel(orig_func):
    def func_wrapper(db_row,project_name,exec_id):
        p=Process(target=orig_func,args=(db_row,project_name,exec_id))
        p.start()
        return p
    return func_wrapper


def multiprocess_join(orig_func):
    def func_wrapper(project_name,exec_id):
        proc_list=orig_func(project_name,exec_id)
        print '===start==='
        print proc_list;
        print '===end==='
        for p in proc_list:
            p.join()
    return func_wrapper


def execute_shell(shell_script_path):
    subprocess.call(['sh '+shell_script_path],shell=True)
    return
