"""

This module deals with job related manipulations. In expresso, job is
understood as a subtask which needs to be performed to get expected result.
Job config is a file which gives you complete information related to this
subtask.
For the bellow documented functions, the job_config_path will be as follow :

.. code-block :: proto
    :name: sample_job_config.prototxt
    :caption: sample_job_config.prototxt

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

The job config is parsed according to the structure defined by
protocol as shown bellow. It is  mandatory to specify the highlighted fields in
the job config file. The parent paths are supposed to be imported from the
pre-defined parent modules available for users. These parent modules
are present for both job and its arguments. They lay foundation for
structure of user specified job config files in prototxt format. Each parent module
can be uniquely identified by (type,category).

.. code-block :: proto
    :name: expresso.proto
    :caption: expresso.proto
    :emphasize-lines: 3,16,30,35
    :linenos:

    message Job {
      optional string name=25;
      optional string type=1; //IO,Train,Benchmark,Transform
      optional string desc=2;// Description of Job Conf
      optional string doc_path=3;// Documentation of Job
      repeated string category=4;
      repeated Arg data=5;//Data related Arguments
      repeated Arg config=6;//Config related Arguments
      optional string script_path=7;// Path of main script to be executed
      optional string depends_on =8;// Dependended Jobs
      optional string pre_exec_rules_path=9;// rules to be checked just before job executes
      optional string post_exec_rules_path=10;//rules to be checked just after the job is executed.
      optional string prereq_install_path=11;// Install all the pre-requisites required for job
      optional string prereq_check_path=12;// Check for pre-requisites
      optional string log_path=13;// Location where job logs will be kept
      optional string job_config_path=14;//Necessary to specify Inputs and Outputs properly
      optional string job_config_proto_path=15;//Necessary to specify Inputs and Outputs properly
      optional string parent_doc_path=16;// Documentation of Job
      optional string parent_job_config_path=17;
      optional string parent_job_config_proto_path=18;
      optional string parent_pre_exec_rules_path=19;// rules to be checked just before job executes
      optional string parent_post_exec_rules_path=20;//rules to be checked just after the job is executed.
      optional string parent_prereq_install_path=21;// Install all the pre-requisites required for job
      optional string parent_prereq_check_path=22;// Check for pre-requisites
      optional string parent_log_path=23;// Location where job logs will be kept
      optional string parent_script_path=24;//Parent Script path
    }
    message Arg {
      optional string name =15;//Name oof the job by which it should appear
      optional string type =1;// Name of the data/config
      repeated string category=2;// Type of data - hdf5,etc,
      optional string desc=3;// Description of Arg
      optional string doc_path=4;// Extended Description in rst
      optional string config_proto_path=5;//Required only if type=custom,else overridden
      optional string config_path=6;// Path of config for Data/Config use cases.
      optional string pre_exec_rules_path=7;// rules to be checked just before job executes
      optional string post_exec_rules_path=8;//rules to be checked just after the job is executed.
      optional string parent_doc_path=9;// Extended Description in rst
      optional string parent_config_path=10;//Config of parent to be overwritten by child
      optional string parent_config_proto_path=11;//Required only if type=custom,else overridden
      optional string parent_pre_exec_rules_path=12;//Not to be set by user
      optional string parent_post_exec_rules_path=13;//Not to be set by user
      optional string io_type=14[default='input'];
    }


"""
from __future__ import absolute_import
from google.protobuf import text_format
from ..proto import expresso_pb2
from . import common
import os

main_paths = ['doc_path', 'script_path', 'prereq_install_path', 'log_path',
              'post_exec_rules_path', 'pre_exec_rules_path', 'job_config_path',
              'job_config_proto_path']
arg_paths = ['doc_path', 'config_proto_path', 'config_path',
             'post_exec_rules_path',
             'pre_exec_rules_path']
job_types = ['IO', 'Train', 'Benchmark', 'Transform']


def parse_job(expresso_root=None, job_config_path=None):
    """
    It parses the job prototxt file and returns a protobuf message
    initialized with the input job prototxt file.
    literal blocks ::

        print expresso.utils.parse_job(job_config_path='sample_job_config.prototxt')

    Args:
        expresso_root (string): Path or expresso root directory, mostly it is '/usr/share/expresso'
        job_config_path (string): Path of the Job prototxt which needs to be parsed. Eg. :ref:`sample_job_config.prototxt`

    Returns:
        job (protobuf msg): Job protobuf message with fields parsed as per the job prototxt
        provided

    """
    job = expresso_pb2.Job()
    text_format.Merge(open(job_config_path,
                           'r').read(), job)
    return job



def make_job_paths_absolute(job, job_config_path):
    """
    It converts all the child paths of job to its absolute paths.
    Note:
        Parent Paths are not touched by this function, rather the parent config
        paths are first made absolute and then merged into the user-specified job's config.

    Args:
        job (protobuf msg): Job's Protobuf Message instance
        job_config_path (str): Absolute path of job.

    Returns:
        job (protobuf msg) : Job's Protobuf Message instance with absolute child paths.

    """
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
                                            common.get_file_path(
                                                job_config_path,
                                                job.config[
                                                    idx].__getattribute__(
                                                    path_attr_name)))

    return job


def make_arg_paths_absolute(arg=None, arg_config_path=None):
    """
    It converts all the child paths of arg to its absolute paths.
    Note:
        Parent Paths are not touched by this function, rather the parent config
        paths are first made absolute and then merged into the user-specified arg's config.
    Args:
        arg (protobuf msg): Arg's Protobuf Message instance
        arg_config_path (str): Absolute path of arg(data/config).

    Returns:
        arg (protobuf msg) : Arg's Protobuf Message instance with absolute child paths.
    """
    for path_attr_name in arg_paths:
        if (arg.HasField(path_attr_name)):
            arg.__setattr__(path_attr_name,
                            common.get_file_path(arg_config_path,
                                                 arg.__getattribute__(
                                                     path_attr_name)))

    return arg


def get_category_path(arg=None, type_val='data',
                      expresso_root=None):
    """
    It returns relative path of the parent category in case of job/arg if present.
    Both Job and Arg Protobuf messages are configurable and can be identified by the
    relative paths. The relative path for the  :ref:`sample_job_config.prototxt` is
    going to be as bellow :

    .. code-block:
        $expresso_root/storage/job/computer_vision/dataset/_to_hdf5/mnist_dataset

    Args:
        arg (protobuf msg): Job/Arg's Protobuf Message instance
        type_val (str):  It is message type and belongs to one of job/data/config.

    Returns:
        category_path (str): Category path for the provided protobuf message.
    """

    if type_val == '' or expresso_root == '' \
            or arg is None:
        raise Exception('Empty parameters to construct category path')


    category_rel_path = '/'.join(['_' + cat for cat in arg.category])
    category_path = expresso_root + '/storage/' + type_val + '/' + \
                    category_rel_path + '/' + arg.type
    if (os.path.exists(category_path)):
        return category_path
    else:
        return None


def merge_with_parent_arg(arg=None, arg_type='data', expresso_root=None):
    """
    Merges parent argument configuration with current. This includes,
    predefined tests, config structure, etc.  If you
    want to skip the import, just overwrite the those parent path parameters with
    exclude. Eg parent_config_path="exclude".
    Args:
        arg (protobuf message): Arg's Protobuf Message instance
        arg_type (str): Type of arg. It can be either config arg or data arg
        expresso_root: Path of expresso's installation location. Mostly it is '/usr/share/expresso'

    Returns:
        arg (protobuf message): Updated Arg's Protobuf Message instance with parent config information.

    """
    # Step 1 : Get parent category path for Arg
    parent_arg_path = get_category_path(arg=arg, type_val=arg_type,
                                        expresso_root=expresso_root)

    if (parent_arg_path is None): return arg;
    parent_config_arg = expresso_pb2.Arg()
    text_format.Merge(
        text=open(parent_arg_path + '/main.prototxt', 'r').read(),
        message=parent_config_arg)
    parent_config_arg = make_arg_paths_absolute(arg=parent_config_arg,
                                                arg_config_path=parent_arg_path)

    # Step 2 : Merging Category parent path for Arg
    for path_attr_name in arg_paths:
        if parent_config_arg.HasField(path_attr_name) and not \
                arg.HasField('parent_' + path_attr_name):
            arg.__setattr__('parent_' + path_attr_name,
                            parent_config_arg.__getattribute__(
                                path_attr_name))

    return arg


def merge_with_parent_job(job=None, expresso_root=None):
    """
    Merges parent job configuration with current. This includes,
    predefined tests, config structure, etc. This facilitates reusability and
    structuring of code such that repeated tasks are least required. If you
    want to skip the import, just overwrite the those parent path parameters with
    exclude. Eg parent_config_path="exclude".
    Args:
        job (protobuf message): Job's Protobuf Message instance
        expresso_root: Path of expresso's installation location. Mostly it is '/usr/share/expresso'

    Returns:
        job (protobuf message): Updated Job's Protobuf Message instance with parent config information.


    """
    parent_job_path = get_category_path(arg=job, type_val='job',
                                        expresso_root=expresso_root)

    if parent_job_path is not None:
        # Step 1 : Get parent category path for Job
        parent_config_job = expresso_pb2.Job()
        text_format.Merge(text=open(parent_job_path + '/main.prototxt',
                                    'r').read(),
                          message=parent_config_job)
        parent_config_job = make_job_paths_absolute(job=parent_config_job,
                                                    job_config_path=parent_job_path)

        for path_attr_name in main_paths:
            if parent_config_job.HasField(path_attr_name) and not \
                    job.HasField('parent_' + path_attr_name):
                job.__setattr__('parent_' + path_attr_name,
                                parent_config_job.__getattribute__(
                                    path_attr_name))

    # Step 2 : Merging parent category path for Job


    for idx, data_arg in enumerate(job.data):
        arg_val = merge_with_parent_arg(arg=job.data[idx],
                                        arg_type='data',
                                        expresso_root=expresso_root);
        if arg_val is None: continue
        job.data[idx].CopyFrom(arg_val)

    for idx, data_arg in enumerate(job.config):
        arg_val = merge_with_parent_arg(arg=job.config[idx],
                                        arg_type='config', expresso_root=None);
        if arg_val is None: continue
        job.config[idx].CopyFrom(arg_val)

    return job

def get_job(expresso_root,job_config_path):
    """
    It parses the job config as per job_config_path and returns fully processed and validated Job's protobuf Message.
    Args:
        expresso_root: Path of expresso's installation location. Mostly it is '/usr/share/expresso'
        job_config_path (string): Path of the Job prototxt which needs to be fetched. Eg. :ref:`sample_job_config.prototxt`

    Returns:
        job (protobuf msg): Job protobuf message with fields parsed and merged with its parent configs.

    """
    job=parse_job(expresso_root=expresso_root,job_config_path=job_config_path)
    job=make_job_paths_absolute(job=job,job_config_path=job_config_path)
    job=merge_with_parent_job(job=job,expresso_root=expresso_root)
    return job;


