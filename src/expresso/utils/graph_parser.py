"""
This module deals with job related manipulations. In expresso, job is
understood as a subtask which needs to be performed to get expected result.
Job config is a file which gives you complete information related to this
subtask.

"""
import dag
from . import common
from . import job_parser
from google.protobuf import text_format
from ..proto import expresso_pb2

def validate_dag(schedule_graph):
    """
    It validates the attributes of Graph and also looks into the cyclic
    dependencies in it. It raises an exception in case of DAG Validation Faliure.
    Args:
        schedule_graph: ScheduleGraph Protobuf Message Object
    """
    pass

def create_dag(expresso_root=None,project_path=None):
    """
    It creates a Schedule Graph Object which consists of Job's execution related information.
    Args:
        expresso_root (str): Path of expresso's installation location. Mostly it is '/usr/share/expresso'
        project_path (str): Path of the project folder. It consists of job related subfolders in it.

    Returns:
        schedule_graph (protobuf msg): Parsed Protobuf message capturing all jobs in
         project with its dependency.
    """
    schedule_graph=expresso_pb2.ScheduleGraph()
    project_name=project_path.strip().split('/')[-1];
    if project_name == '':
        raise Exception('Project path is not present')
    schedule_graph.name=project_name #Name of project
    folder_list=common.get_folders(project_path)
    schedule_jobs=[]
    for idx,elem in enumerate(folder_list):
        schedule_jobs.append(expresso_pb2.ScheduleJob())
        schedule_jobs[idx].name=elem
        text_format.Merge(message=schedule_jobs[idx].job,text=str(job_parser.get_job(expresso_root=expresso_root,
                                            job_config_path=project_path+'/'
                                            +elem+'/main.prototxt')))
        schedule_jobs[idx].depends_on.extend(schedule_jobs[idx].job.depends_on.strip().split(","));
    schedule_graph.schedule_job.extend(schedule_jobs)

    validate_dag(schedule_graph)
    return schedule_graph


def graph_to_json(schedule_graph):
    """

    Args:
        schedule_graph: ScheduleGraph Protobuf Message Object

    Returns:
        schedule_graph_json: ScheduleGraph's JSON object

    """
    print schedule_graph

print '-----------'
print create_dag(expresso_root='/usr/share/expresso',project_path='/home/jaley/Projects/project1')
