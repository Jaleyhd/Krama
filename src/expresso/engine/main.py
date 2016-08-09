from __future__ import absolute_import
from ..utils import  common
from ..utils import  job_parser
from . import schedular
import sys
root_path='/usr/share/expresso/proto';

folder_list=common.get_folders(main_folder=sys.args[1])
common.compile_configs(folder_list)
jobs=job_parser.get_jobs(folder_list)
#graph=graph_parser.create_graph(main_folder,jobs)
#dependency_handler.handle_prerequisites(graph)
#graph_parser.generate_shell_script()
#schedular.execute(graph)