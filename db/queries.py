from __future__ import absolute_import
from . import executions_tab
from ..conf import common

executions_tab_handle=executions_tab.Executions_tab()


def db_insert_jobs(schedule_jobs=[],project_name='',exec_id=-1,project_path=''):
    for job_proto in schedule_jobs:
        executions_tab_handle.insert_job(job_proto=job_proto,project_name=project_name,
                                         exec_id=exec_id,project_path=project_path)
    open(common.EXECUTION_UPDATE_TRIGGER_PATH,
         'w').write(project_path.replace("'", "") +
                    '/.executions/exec_' + exec_id + '/main.json')


def db_update_status(db_row,status):
    db_row[common.EXECUTIONS_TAB_COLUMN_STATUS]=status
    executions_tab_handle.update_row(row=db_row);

def db_get_all_jobs(project_name,exec_id):
    return executions_tab_handle.get_all_jobs_executions_tab(project_name,exec_id)

def db_get_all():
    return executions_tab_handle.get_all_executions_tab()


def db_reset_fail_jobs(project_name,exec_id):
    for row in db_get_all_jobs(project_name,exec_id):
        if row[common.EXECUTIONS_TAB_COLUMN_STATUS]==common.EXECUTION_STATUS_FAIL:
            row[common.EXECUTIONS_TAB_COLUMN_STATUS]=common.EXECUTION_STATUS_UNKNOWN

def close():
    executions_tab_handle.close()


