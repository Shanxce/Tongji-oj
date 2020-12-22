import time
from . import config
import logging
import sqlite3
import time

def get_task():
    sql = "select solution_id,problem_id,problem_lang,user_id from Solutions where judge_state=\"waiting\""
    time.sleep(1)
    ans = run_sql(sql)
    print("get_task:",ans)
    if ans is None:
        logging.error("do not get task!")
        return None
    else:
        return ans
def update_result(result):
    sql = "update Solutions set judge_state=\"%s\",pass_case=%d,time_used=%d,mem_used=%d where solution_id=%d" \
            % (config.result_sig[result['result']], result['pass_point'], \
            result['take_time'], result['take_memory'], \
            result['solution_id'])
    print("sqlresult:",result)
    run_sql(sql)


def get_code_fail(solution_id):
    print("get_code_fail")
    sql="update Solutions set judge_state=\'%s\',\
        pass_case=%d,time_used=%d,mem_used=%f \
            where solution_id=%d" % ('SE', 0, 0, 0, solution_id)

    run_sql(sql)

def get_problem_limit(problem_id):
    sql='select time_limit,memory_limit from OJProblems where problem_id=%d'%(problem_id)
    
    limits = run_sql(sql)
    limits = limits[0]
    print(limits)
    time_limit,memory_limit=limits
    if time_limit is None or memory_limit is None :
        return None, None
    else:
        return time_limit,memory_limit

def run_sql(sql):
    con = None
    while True:
        try:
            con = sqlite3.connect(config.database)
            break
        except: 
            logging.error('Cannot connect to database,trying again')
            time.sleep(1)
    try:
        cur = con.cursor()
        if isinstance(sql,str):
            cur.execute(sql)
        elif isinstance(sql,list):
            for i in sql:
                cur.execute(i)
    except sqlite3.OperationalError as e:
        logging.error(e)
        cur.close()
        con.close()
        return False
    con.commit()
    data = cur.fetchall()
    cur.close()
    con.close()
    print("sqlline:",sql)
    print("data:",data)
    return data



