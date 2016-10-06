from __future__  import absolute_import
from ..utils import graph_parser
from pprint import pprint
import sys
from ..conf.common import bcolors
from ..conf import common
from ..display import job_monitor
global_option_list=['print','ps']

def parse_args():
    arg_dict={'option':'','flag':'','arg':'','aux_options':{}}
    optionpos = {idx:elem[1:] for idx,elem in enumerate(sys.argv[1:]) if
                 elem.startswith('-') and len(elem)>1 and not elem.startswith('--')}
    flagpos = {idx:elem[2:] for idx,elem in enumerate(sys.argv[1:]) if
               elem.startswith('--') and len(elem)>2}
    argpos = {idx:elem for idx,elem in enumerate(sys.argv[1:]) if
                  not elem.startswith('-') and len(elem)>0}



    if len(optionpos)>0 :arg_dict['option']=optionpos.values()[0]
    if(len(optionpos)<=1):
        if len(flagpos)>0 :arg_dict['flag']=flagpos.values()[0]
        if len(argpos) > 0: arg_dict['arg'] = argpos.values()[0]
    else:
        if len(flagpos)>0 and flagpos.keys()[0]<optionpos.keys()[1]:arg_dict['flag']=flagpos.values()[0]
        if len(argpos) >0 and argpos.keys()[0]<optionpos.keys()[1]: arg_dict['arg'] = argpos.values()[0]

    #Options apart from primary option
    for idx,op in enumerate(optionpos.keys()[1:-1]):
        opplus=optionpos.keys()[2+idx]
        fp=[fp for fp in flagpos if fp>op and fp<opplus ]
        fp=fp[0] if len(fp)>0 else -1
        ap = [ap for ap in argpos if ap > op and ap < opplus]
        ap = ap[0] if len(ap)>0 else -1
        print ap, op,opplus
        arg_dict['aux_options'][optionpos[op]]={'flag':flagpos[fp]  if fp>=0 else '',
                                                 'arg':argpos[ap]  if ap>=0 else ''}
    for idx,op in enumerate(optionpos.keys()[1:][-1:]):
        fp=[fp for fp in flagpos if fp>op  ]
        fp=fp[0] if len(fp)>0 else -1
        ap = [ap for ap in argpos if ap > op]
        ap = ap[0] if len(ap)>0 else -1
        arg_dict['aux_options'][optionpos[op]] = {'flag': flagpos[fp] if fp>=0 else '',
                                                 'arg': argpos[ap] if ap>=0 else ''}

    return arg_dict


def option_print_func(arg_dict,krama_root):
    if(arg_dict['flag'] is ''):
        graph_obj=graph_parser.create_dag(krama_root=krama_root,project_path='/home/jaley/Projects/project1')
        graph_parser.print_graph_json(graph_obj)

def option_ps_func(arg_dict,krama_root):
    job_monitor.display()

def is_valid_option(arg_dict,option_list):
    return ('option' in arg_dict) and (arg_dict['option'] in option_list)

def default_message():
    print ''
    print bcolors.HEADER+bcolors.UNDERLINE +'Krama Usage : krama <options> <flag> <file/folder>'+bcolors.ENDC+bcolors.ENDC
    print bcolors.OKBLUE  + 'krama -print <folderpath>'+bcolors.ENDC+'\t\t\t Prints Task Dependency Graph  in json format'
    print bcolors.OKBLUE  + 'krama -print '+bcolors.ENDC
    print bcolors.WARNING + '\t\t--proto <folderpath>'  + '\t\t\t in prototxt format'+ bcolors.ENDC
    print bcolors.WARNING + '\t\t--names <folderpath>' + '\t\t\t only task names' + bcolors.ENDC
    print ''
    print bcolors.OKBLUE  + 'krama -save <folderpath>' + bcolors.ENDC + '\t\t\t Prints Task Dependency Graph  in json format'
    print bcolors.OKBLUE  + 'krama -save ' + bcolors.ENDC
    print bcolors.WARNING + '\t\t--proto -input <folderpath> -output <filepath>' + '\t\t\t in prototxt format' + bcolors.ENDC
    print bcolors.WARNING + '\t\t--names -input <folderpath> -output <filepath>' + '\t\t\t only task names' + bcolors.ENDC
    print bcolors.OKBLUE  + 'krama -ps '+'\t\t\t show recently run jobs'+bcolors.ENDC
    print ''

if __name__ =="__main__":
    arg_dict=parse_args()
    if len(sys.argv)==1:default_message()
    if is_valid_option(arg_dict=arg_dict,option_list=global_option_list): locals()['option_'+arg_dict['option']+'_func'](arg_dict=arg_dict,krama_root=common.KRAMA_ROOT)
