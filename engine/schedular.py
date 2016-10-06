from __future__ import absolute_import
from ..utils import graph_parser
import os
from time import sleep
import multiprocessing
import sys
from multiprocessing import Process
from . import process_util

def execute(project_path,krama_root):
    graph_proto=graph_parser.create_dag(project_path=project_path,krama_root=krama_root)
    open(os.path.join(project_path,'main.prototxt'),'w').write(str(graph_proto))
    current_exec_path=initalize_execution(graph_proto=graph_proto,project_path=project_path)
    execute_graph(graph_proto=graph_proto
                  ,current_exec_path=current_exec_path)


def get_next(execution_path):
    execlist=[int(elem[5:]) for elem in os.listdir(execution_path) if
              elem.startswith('exec_')  and os.path.isdir(os.path.join(execution_path,elem))]
    if len(execlist)==0:
        return 0
    else:
        return max(execlist)+1

def initalize_execution(graph_proto,project_path):
    execution_path=os.path.join(project_path,'.executions');
    if not os.path.exists(execution_path):
        os.mkdir(execution_path)
    current_exec_path=os.path.join(execution_path, 'exec_'+str(get_next(execution_path=execution_path)))
    os.mkdir(current_exec_path)
    open(os.path.join(current_exec_path,'main.prototxt'),'w').write(str(graph_proto))
    return current_exec_path


def get_independent_jobs(graph_proto):
    job_queue=[]
    for schedule_job in graph_proto.schedule_job:
        if len(schedule_job.depends_on)==0:job_queue.append(schedule_job)
    return job_queue

def execute_graph(graph_proto,current_exec_path):
    process_util.process(schedule_jobs=graph_proto.schedule_job,current_exec_path=current_exec_path)


if __name__=="__main__":
    execute(project_path='/home/jaley/Projects/project1',krama_root='/usr/share/krama')