from __future__ import absolute_import
from . import db_util
from ..proto import krama_pb2
from ..conf import common
import MySQLdb
import os
from google.protobuf import text_format
import simplejson
from ..protobufjson.protobuf_json import *

# CREATE TABLE executions_tab
# (
# exec_id INT NOT NULL AUTO_INCREMENT,
# job_name VARCHAR(512),
# project_name VARCHAR(512),
# depends_on VARCHAR(2048),
# status INT NOT NULL,
# start_time BIGINT DEFAULT -1,
# end_time  BIGINT DEFAULT -1,
# retry INT,
# pid INT,
# completion_percentage FLOAT DEFAULT -1.0,
# PRIMARY KEY(exec  _id,job_name)
# )

{
    "exec_id":{"value":"","data_type":"float"}
}

class Executions_tab:
    def __init__(self):
        self.db=db_util.DbUtil()

    def insert_job(self,job_proto,project_name,exec_id,project_path):
        arg_dict=self.proto_to_arg_dict(job_proto=job_proto,
                                        project_name=project_name,exec_id=exec_id
                                        ,project_path=project_path)
        self.insert_dict(arg_dict)

    def update_job(self,job_proto,project_name,exec_id):
        arg_dict=self.proto_to_arg_dict(job_proto=job_proto,
                                        project_name=project_name,exec_id=exec_id)
        self.update_dict(arg_dict)


    def update_row(self,row):
        self.update_proto(row)
        arg_dict=self.row_to_arg_dict(db_job=row)
        self.update_dict(arg_dict=arg_dict)

    def update_proto(self,row):
        """
        Updates the execution prototxt
        Args:
            row:

        Returns:
        """
        current_exec_path=row["project_path"]+'/.executions/exec_'+str(row["exec_id"])
        current_exec_proto_path=current_exec_path+'/main.prototxt'
        current_exec_json_path=current_exec_path+'/main.json'
        if os.path.exists(current_exec_path) and os.path.exists(current_exec_proto_path):
            schedule_graph=krama_pb2.ScheduleGraph()
            text_format.Merge(text=open(current_exec_proto_path).read(),message=schedule_graph)
            for idx,schedule_job in enumerate(schedule_graph.schedule_job):
                if str(schedule_job.name) == row["job_name"]:
                    schedule_graph.schedule_job[idx].status=common.EXECUTION_STATUS_DICT[int(str(row["status"]))]

            open(current_exec_proto_path,'w').write(str(schedule_graph))
        open(current_exec_json_path, 'w').write(simplejson.dumps(pb2json(schedule_graph)))

    #@staticmethod
    def row_to_arg_dict(self,db_job):
        arg_dict={}
        #1 exec_id
        arg_dict['exec_id']=str(db_job['exec_id'])
        #2 project_name
        arg_dict['project_name']="'"+str(db_job['project_name'])+"'"
        #3 project_name
        arg_dict['project_path']="'"+str(db_job['project_path'])+"'"
        #4 job_name
        arg_dict['job_name']="'"+str(db_job['job_name'])+"'"
        #5 depends_on
        arg_dict['depends_on']="'"+str(db_job['depends_on'])+"'"
        #6 status
        arg_dict['status']=str(db_job['status'])
        #7 pid
        arg_dict['pid']=str(db_job['pid'])
        #8 start_time
        arg_dict['start_time']=str(db_job['start_time'])
        #9 end_time
        arg_dict['end_time']=str(db_job['end_time'])
        #10 retry
        arg_dict['retry']=str(db_job['retry'])
        #11 completion_percentage
        arg_dict['completion_percentage']=str(db_job['completion_percentage'])
        return arg_dict


    #@staticmethod
    def proto_to_arg_dict(self,job_proto,project_name,exec_id,project_path):
        arg_dict={}
        #1 exec_id
        arg_dict['exec_id']=str(exec_id)
        #2 project_name
        arg_dict['project_name']="'"+str(project_name)+"'"
        #3 project_path
        arg_dict['project_path']="'"+str(project_path)+"'"
        #4 job_name
        if job_proto.HasField('name') and len(str(job_proto.name))>0:
            arg_dict['job_name']="'"+str(job_proto.name)+"'"
        #5 depends_on
        arg_dict['depends_on']="'"+str(','.join(job_proto.depends_on))+"'"
        #6 status
        if job_proto.HasField('status') and len(str(job_proto.status))>0:
            arg_dict['status']=str(job_proto.depends_on)
        else:
            arg_dict['status']=str(common.EXECUTION_STATUS_UNKNOWN)
        #7 pid
        if job_proto.HasField('pid') and len(str(job_proto.pid))>0:
            arg_dict['pid']=str(job_proto.pid)
        #8 start_time
        if job_proto.HasField('start_time') and len(str(job_proto.start_time))>0:
            arg_dict['start_time']=str(job_proto.start_time)
        #9 end_time
        if job_proto.HasField('end_time') and len(str(job_proto.end_time))>0:
            arg_dict['end_time']=str(job_proto.end_time)
        #10 retry
        if job_proto.HasField('retry') and len(str(job_proto.retry))>0:
            arg_dict['retry']=str(job_proto.retry)
        else:
            arg_dict['retry']=str(common.DEFAULT_EXECUTION_RETRY)
        #11 completion_percentage
        if job_proto.HasField('completion_percentage') and len(str(job_proto.completion_percentage))>0:
            arg_dict['completion_percentage']=str(job_proto.completion_percentage)
        else:
            arg_dict['completion_percentage']=str(common.DEFAULT_EXECUTION_COMPLETION_PERC)

        return arg_dict



    def insert_dict(self,arg_dict):
        statement="INSERT INTO executions_tab ("+str(",".join(arg_dict.keys()))+\
                  ") VALUES ("+str(','.join(arg_dict.values()))+");"

        self.db.execute(statement=statement)


    def update_dict(self,arg_dict):
        statement=""
        statement="UPDATE executions_tab SET "+str(", ".join([k+'='+v for (k,v) in arg_dict.items() ]))+\
                  " WHERE "+str(' and '.join([k+'='+v for (k,v) in arg_dict.items()
                                         if k in common.EXECUTIONS_TAB_PRIMARY_KEYS]))+";"

        self.db.execute(statement=statement)
        open(common.EXECUTION_UPDATE_TRIGGER_PATH,
             'w').write(arg_dict["project_path"].replace("'","")+
                        '/.executions/exec_'+arg_dict['exec_id']+'/main.json')



    def get_all_jobs_executions_tab(self,project_name,exec_id):
        statement="SELECT * FROM executions_tab where project_name='"+str(project_name)\
                  +"' and exec_id="+str(exec_id)+";"
        return self.db.fetch_dict(statement)

    def get_all_executions_tab(self):
        statement="SELECT * FROM executions_tab";
        return self.db.fetch_dict(statement)

    def close(self):
        self.db.close()

if __name__=="__main__":
    e=Executions_tab()