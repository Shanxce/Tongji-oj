
from . import config
from .sqlwork import run_sql
import logging
import os
def get_code(solution_id, problem_id, pro_lang):
    '''从数据库获取代码并写入work目录下对应的文件'''
    file_name = {
        "gcc": "main.c",
        "g++": "main.cpp",
        'python3': 'main.py'
    }
    select_code_sql = "select code_string from Solutions where solution_id=%d"%(solution_id)
    feh = run_sql(select_code_sql)
    if feh is not None:
        try:
            code = feh[0][0]
        except:
            logging.error("1 cannot get code of runid %s" % solution_id)
            return False
    else:
        logging.error("2 cannot get code of runid %s" % solution_id)
        return False
    try:
        work_path = os.path.join(config.work_dir, str(solution_id))
        os.mkdir(work_path)
    except OSError as e:
        if str(e).find("exist") > 0:  # 文件夹已经存在
            pass
        else:
            logging.error(e)
            return False
    try:
        real_path = os.path.join(
            config.work_dir,
            str(solution_id),
            file_name[str(pro_lang)])
    except KeyError as e:
        logging.error(e)
        return False
    try:
        f = open(real_path, 'w')
        try:
            f.write(code)
        except:
            logging.error("%s not write code to file" % solution_id)
            f.close()
            return False
        f.close()
    except OSError as e:
        logging.error(e)
        return False
    return True