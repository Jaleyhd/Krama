from __future__ import absolute_import

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Default Parameters
DEFAULT_EXECUTION_RETRY=0
DEFAULT_EXECUTION_COMPLETION_PERC=0.0

EXECUTION_STATUS_FAIL=0
EXECUTION_STATUS_SUCCESS=1
EXECUTION_STATUS_RUN=2
EXECUTION_STATUS_CANCEL=3
EXECUTION_STATUS_UNKNOWN=5

EXECUTION_STATUS_DICT={
    EXECUTION_STATUS_FAIL:"FAIL",
    EXECUTION_STATUS_SUCCESS:"SUCCESS",
    EXECUTION_STATUS_RUN:"RUN",
    EXECUTION_STATUS_CANCEL:"CANCEL",
    EXECUTION_STATUS_UNKNOWN:"UNKNOWN"
}

EXECUTIONS_TAB_COLUMN_STATUS='status'

EXECUTIONS_TAB_PRIMARY_KEYS=['exec_id','project_name','job_name']

KRAMA_ROOT='/usr/share/krama'

EXECUTION_UPDATE_TRIGGER_PATH='/usr/share/krama/web/refresh.txt'



CAFFE_ROOT='/home/jaley/caffe'
