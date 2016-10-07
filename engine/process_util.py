from ..db import queries
from .process_core import *
from time import sleep
from ..conf import common
from .executions import *
import random

def process(schedule_jobs,current_exec_path):
    exec_id=str(current_exec_path.split('/')[-1][5:])
    project_name=current_exec_path.split('/')[-3]
    project_path='/'.join(current_exec_path.split('/')[:-2])
    print project_name,project_path,exec_id
    queries.db_insert_jobs(schedule_jobs,project_name=project_name,exec_id=exec_id,project_path=project_path)
    process_next_jobs(project_name=project_name,exec_id=exec_id)


def is_independent(depends_on,sucessful_jobs):
    depends_on=depends_on.strip().split(',')
    for elem in sucessful_jobs:
        if elem in depends_on:depends_on.remove(elem)
    if '' in depends_on:depends_on.remove('')
    return len(depends_on)==0

def get_independent_jobs(project_name,exec_id):
    db_jobs=queries.db_get_all_jobs(project_name=project_name,exec_id=exec_id)
    sucessful_jobs=[row['job_name'] for row in db_jobs
                    if row[common.EXECUTIONS_TAB_COLUMN_STATUS]==common.EXECUTION_STATUS_SUCCESS]
    independent_jobs=[row for row in db_jobs if is_independent(row['depends_on'],sucessful_jobs) and
                      row[common.EXECUTIONS_TAB_COLUMN_STATUS]==common.EXECUTION_STATUS_UNKNOWN]
    return independent_jobs


def get_execution_script(schedule_job):
    pass

@multiprocess_join
def process_next_jobs(project_name,exec_id):
    proc_list=[]
    for db_row in get_independent_jobs(project_name=project_name,exec_id=exec_id):
        proc_list.append(process_job(db_row=db_row,project_name=project_name,exec_id=exec_id))
    return proc_list

@multiprocess_parallel
def process_job(db_row,project_name,exec_id):
    try:
        queries.db_update_status(db_row=db_row,status=common.EXECUTION_STATUS_RUN)
        filepath=db_row['project_path']+'/'+db_row['job_name']+'/script.sh'
        execute_shell(filepath)
        #sleep(random.randint(1, 6)+random.random()*2)
        queries.db_update_status(db_row=db_row,status=common.EXECUTION_STATUS_SUCCESS)
    except Exception:
        print 'Exception'
        queries.db_update_status(db_row=db_row,
                                   status=common.EXECUTION_STATUS_FAIL)
    process_next_jobs(project_name=project_name,exec_id=exec_id)

