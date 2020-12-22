import os
from . import config
import threading
from .judge import judge
from .compile_code import compile_code
from .sqlwork import *
from .check_code import check_dangerous_code
from .get_code import get_code
def get_data_count(problem_id):
    data_dir = os.path.join(config.data_dir, str(problem_id), 'test_data')
    print("data_dir",data_dir)
    try:
        files = os.listdir(data_dir)
        print("files",files)
    except OSError as e:
        logging.error(e)
        return 0
    count = 0
    for file in files:
        if file.endswith(".in") and file.startswith("data"):
            count += 1
    return count    

def clear_work_dir(solution_id):
    dir_name = os.path.join(config.work_dir, str(solution_id))
    shutil.rmtree(dir_name)

def run(problem_id, solution_id, language, data_count, user_id):
    '''获取程序执行时间和内存'''
    result_code = {
        "Waiting": 0,
        "Accepted": 1,
        "Time Limit Exceeded": 2,
        "Memory Limit Exceeded": 3,
        "Wrong Answer": 4,
        "Runtime Error": 5,
        "Output limit": 6,
        "Compile Error": 7,
        "Presentation Error": 8,
        "System Error": 11,
        "Judging": 12,
    }
    program_info = {
        "solution_id": solution_id,
        "problem_id": problem_id,
        "take_time": 0,
        "take_memory": 0,
        "pass_point":0,
        "user_id": user_id,
        "result": 0,
    }
    time_limit, mem_limit = get_problem_limit(problem_id)
    if time_limit is None:
        logging.error("cannot get the limit of pro_id : %d" % problem_id)
        program_info['result']=result_code['System Error']
        return program_info

    if check_dangerous_code(solution_id, language) == False:
        program_info['result'] = result_code["Runtime Error"]
        return program_info
    compile_result = compile_code(solution_id, language)
    if compile_result is False:  # 编译错误
        program_info['result'] = result_code["Compile Error"]
        return program_info
    if data_count == 0:  # 没有测试数据
        program_info['result'] = result_code["System Error"]
        print("no data_count")
        return program_info
    result = judge(
        solution_id,
        problem_id,
        user_id,
        data_count,
        time_limit,
        mem_limit,
        program_info,
        result_code,
        language)
    logging.debug(result)
    return result


def worker(solution_id, problem_id, language, user_id):
    data_count = get_data_count(problem_id)  # 获取测试数据的个数
    if(get_code(solution_id,problem_id,language)==False):
        get_code_fail(solution_id)
        return False
    logging.info("judging %s" % solution_id)
    result = run(
        problem_id,
        solution_id,
        language,
        data_count,
        user_id,)  # 评判ss
    logging.info(
    "%s result %s" % (
        result[
    'solution_id'],
        result[
    'result']))
    update_result(result)  # 将结果写入数据库
    if config.auto_clean:  # 清理work目录
        clean_work_dir(result['solution_id'])
def mainwork():
    tasks = get_task()
    for task in tasks:
        print("istask",task)
        solution_id, problem_id, language, user_id=task
        worker(solution_id, problem_id, language, user_id)

if __name__ == 'main':
    mainwork()
