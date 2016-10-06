from __future__ import absolute_import
import unicurses
import curses
from time import sleep
from ..db import queries
from pprint import pprint
from tabulate import tabulate

def dict2tab(ary_dict):
    headers=["exec_id","job_name","project_name","status"]
    if len(ary_dict)==0:return {"headers":[],"table":[]}
    last_3_execs=sorted(list(set([int(elem['exec_id']) for elem in ary_dict ])))
    table=[[elem[k] for k in headers ] for elem in ary_dict if elem['exec_id'] in last_3_execs[-3:]]
    return {"headers":headers,"table":table}
    #return {"headers":list(ary_dict[0].keys()),"table":[list(elem.values()) for elem in ary_dict if elem['exec_id']==73]}

def recolor(sc,print_data,result):
    header_color_id=10
    current_exec_color_id=2
    curses.start_color()
    curses.init_pair(10,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_MAGENTA,curses.COLOR_BLACK)
    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_BLUE,curses.COLOR_WHITE)
    curses.init_pair(4,curses.COLOR_MAGENTA,curses.COLOR_BLACK)
    curses.init_pair(6,curses.COLOR_BLUE,curses.COLOR_BLACK)

    sc.addstr('\n'.join(print_data.split('\n')[0:3]) + '\n',
              curses.color_pair(10))
    for idx,lines in enumerate(print_data.split('\n')[3:]):
        print int(result["table"][int(idx/2)][-1])+1
        sc.addstr(lines+'\n',curses.color_pair(int(result["table"][int(idx/2)][-1])+1))

def printscr(sc):
    sc.nodelay(1)
    while True:
        result = dict2tab(queries.db_get_all())
        print_data=tabulate(tabular_data=result["table"],headers=result['headers'],tablefmt="fancy_grid").encode('utf-8')
        recolor(sc=sc,print_data=print_data,result=result)
        sc.refresh()
        if sc.getch() == ord('q'):
            break
        sleep(1)
        sc.clear()
    #unicurses.endwin()
    return 0


def display():
    curses.wrapper(printscr)


if __name__=='__main__':
    pass