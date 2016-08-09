from __future__ import absolute_import
from google.protobuf import text_format
from ..proto import expresso_pb2
from . import common
import os
"""
job_parser
----------------------
This module deals with job related manipulations. In expresso, job is
understood as a subtask which needs to be performed to get expected result.
Job config is a file which gives you complete information related to this
subtask.
For the bellow documented functions, the job_config_path will be as follow :
literal blocks::
    name: "job1"
    type: "mnist_to_hdf5"
    category: "computer_vision"
    category: "dataset"
    category: "to_hdf5"
    desc: "Importing mnist dataset in hdf5"
    data {
      name: "mnist_import"
      type: "mnist_import"
      category: "machine_learning"
      desc: "Import mnist data from net"
      config_path: "./data_config.prototxt"
    }
    log_path: "log"
"""

main_paths = ['doc_path', 'script_path', 'prereq_install_path', 'log_path',
              'post_exec_rules_path', 'pre_exec_rules_path','job_config_path',
              'job_config_proto_path']
arg_paths = ['doc_path', 'config_proto_path', 'config_path',
             'post_exec_rules_path',
             'pre_exec_rules_path']
job_types = ['IO', 'Train', 'Benchmark', 'Transform']



def parse_job(expresso_root=None, job_config_path=None):
    """
    It parses the job prototxt file and returns a protobuf message
    initialized with the input job prototxt file.
    literal blocks::

        print expresso.utils.parse_job(job_config_path='my_job_config_path.prototxt')

    Args:
        expresso_root(not required): Path or expresso root directory, mostly
        it is
        '/usr/share/expresso'
        job_config_path: Path of the Job prototxt which needs to be parsed

    Returns:
        Job protobuf message with fields parsed as per the job prototxt
        provided

    literal blocks::
        name: "job1"
        type: "mnist_to_hdf5"
        category: "computer_vision"
        category: "dataset"
        category: "to_hdf5"
        desc: "Importing mnist dataset in hdf5"
        data {
          name: "mnist_import"
          type: "mnist_import"
          category: "machine_learning"
          desc: "Import mnist data from net"
          config_path: "./data_config.prototxt"
        }
        log_path: "log"

    """
    job = expresso_pb2.Job()
    text_format.Merge(open('/usr/share/expresso/proto/jobexample.prototxt',
                           'r').read(), job)
    return job


def make_job_paths_absolute(job, job_config_path):
    for path_attr_name in main_paths:
        if (job.HasField(path_attr_name)):
            job.__setattr__(path_attr_name,
                            common.get_file_path(job_config_path,
                                                 job.__getattribute__(
                                                     path_attr_name)))

    for idx, data_arg in enumerate(job.data):
        for path_attr_name in arg_paths:
            if (job.data[idx].HasField(path_attr_name)):
                job.data[idx].__setattr__(path_attr_name,
                                          common.get_file_path(job_config_path,
                                                               job.data[
                                                                   idx].__getattribute__(
                                                                   path_attr_name)))

    for idx, config_arg in enumerate(job.config):
        for path_attr_name in arg_paths:
            if (job.config[idx].HasField(path_attr_name)):
                job.config[idx].__setattr__(path_attr_name,
                                          common.get_file_path(job_config_path,
                                                               job.config[
                                                                   idx].__getattribute__(
                                                                   path_attr_name)))


    return job

def make_arg_paths_absolute(arg=None, arg_config_path=None):
    for path_attr_name in arg_paths:
        if (arg.HasField(path_attr_name)):
            arg.__setattr__(path_attr_name,
                                      common.get_file_path(arg_config_path,
                                                           arg.__getattribute__(
                                                               path_attr_name)))

    return arg

def get_category_path(arg=None, type_val='data',
                      expresso_root=None):
    if type_val == '' or expresso_root == '' \
            or arg is None:
        raise Exception('Empty parameters to construct category path')

    category_rel_path = '/'.join(['_' + cat for cat in arg.category])
    category_path = expresso_root + '/storage/' + type_val + '/' + \
      category_rel_path + '/' + arg.type
    print category_path
    if(os.path.exists(category_path)):
        return category_path
    else : return None


def merge_with_parent_arg(arg=None,arg_type='data',expresso_root=None):
    # Step 1 : Get parent category path for Arg
    parent_arg_path = get_category_path(arg=arg, type_val=arg_type,
                                     expresso_root=expresso_root)

    if (parent_arg_path is None): return arg;
    parent_config_arg = expresso_pb2.Arg()
    text_format.Merge(text=open(parent_arg_path + '/main.prototxt', 'r').read(),
                      message=parent_config_arg)
    parent_config_arg = make_arg_paths_absolute(arg=parent_config_arg,
                                             arg_config_path=parent_arg_path)

    # Step 2 : Merging Category parent path for Arg
    for path_attr_name in arg_paths:
        if parent_config_arg.HasField(path_attr_name) and not \
                arg.HasField('parent_'+path_attr_name):
            arg.__setattr__('parent_'+path_attr_name,
                            parent_config_arg.__getattribute__(
                                                               path_attr_name))


    return arg


def merge_with_parent_job(job=None,expresso_root=None):

    parent_job_path = get_category_path(arg=job, type_val='job',
                                     expresso_root=expresso_root)

    if parent_job_path is not None:
        # Step 1 : Get parent category path for Job
        parent_config_job = expresso_pb2.Job()
        text_format.Merge(text=open(parent_job_path + '/main.prototxt',
                                    'r').read(),
                          message=parent_config_job)
        parent_config_job  = make_job_paths_absolute(job=parent_config_job,
                                                    job_config_path=parent_job_path)

        for path_attr_name in main_paths:
            if parent_config_job.HasField(path_attr_name) and not \
                    job.HasField('parent_'+path_attr_name):
                print path_attr_name+'123'
                job.__setattr__('parent_'+path_attr_name,
                                parent_config_job.__getattribute__(
                                                                   path_attr_name))


    # Step 2 : Merging parent category path for Job


    for idx,data_arg in enumerate(job.data):
        arg_val=merge_with_parent_arg(arg=job.data[idx],
                                      arg_type='data',expresso_root=expresso_root);
        if arg_val is None: continue
        job.data[idx].CopyFrom(arg_val)

    for idx,data_arg in enumerate(job.config):
        arg_val=merge_with_parent_arg(arg=job.config[idx],
                                      arg_type='config',expresso_root=None);
        if arg_val is None: continue
        job.config[idx].CopyFrom(arg_val)

    return job

job = parse_job(expresso_root='/usr/share/expresso',
                job_config_path='/usr/share/expresso/proto/jobexample.prototxt')
job = make_job_paths_absolute(job,'/usr/share/expresso/proto')

job = merge_with_parent_job(job=job,expresso_root='/usr/share/expresso')
print job;
