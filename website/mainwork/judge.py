import os
from . import config
import sys
import logging
sys.path.append("../Lo-runner")
import lorun
import shlex

def judge_result(problem_id, solution_id, data_num):
    logging.debug("Judging result")
    correct_result = os.path.join(
        config.data_dir, str(problem_id),"test_data", 'data%s.out' %
        data_num)
    print(correct_result)
    user_result = os.path.join(
        config.work_dir, str(solution_id), 'out%s.txt' %
        data_num)
    print(user_result)
    try:
        # 删除\r,删除行末的空格和换行
        correct = open(correct_result,'r').read().replace('\r', '').rstrip()
        user = open(user_result,'r').read().replace('\r', '').rstrip()
    except:
        return False
    
    if correct == user:  # 完全相同:AC
        return "Accepted"
    if correct.split() == user.split():  # 除去空格,tab,换行相同:PE
        return "Presentation Error"
    if correct in user:  # 输出多了
        return "Output limit"
    return "Wrong Answer"  # 其他WA

def judge_one_mem_time(
        solution_id, problem_id, data_num, time_limit, mem_limit, language):

    '''评测一组数据'''
    input_path = os.path.join(
        config.data_dir, str(problem_id),"test_data", 'data%s.in' %
        data_num)

    print("inputpath:",input_path)
    try:
        input_data = open(input_path,'r')
    except:
        return False
    output_path = os.path.join(
        config.work_dir, str(solution_id), 'out%s.txt' %
        data_num)
    print("out_path",output_path)
    temp_out_data = open(output_path, 'w')
    print(temp_out_data)
    if language == 'python3':
        cmd = 'python3 %s' % (
            os.path.join(config.work_dir,
                         str(solution_id),
                         '__pycache__/main.cpython-38.pyc'))
        main_exe = shlex.split(cmd)
    else:
        main_exe = [os.path.join(config.work_dir, str(solution_id), 'main'), ]
    runcfg = {
        'args': main_exe,
        'fd_in': input_data.fileno(),
        'fd_out': temp_out_data.fileno(),
        'timelimit': time_limit,  # in MS
        'memorylimit': mem_limit,  # in KB
        'trace' : True,
        'calls': [1,3, 17, 12, 21, 257, 5, 9, 0, 10, 158, 11, 8, 218,\
            89,63,231], # system calls that could be used by testing programs
        'files' : {'/etc/ld.so.cache': 1} # open flag permitted (value is the flags of open)
    }
    rst = lorun.run(runcfg)
    print("lorn:",rst)
    input_data.close()
    temp_out_data.close()
    logging.debug(rst)
    return rst


def judge(solution_id, problem_id,user_id, data_count, time_limit,
          mem_limit, program_info, result_code, language):
    '''评测编译类型语言'''
    max_mem = 0
    max_time = 0
    #if language =='python3':
    #    time_limit = time_limit * 2
     #   mem_limit = mem_limit * 2
    for i in range(data_count):
        ret = judge_one_mem_time(
            solution_id,
            problem_id,
            i+1,
            time_limit + 10,
            mem_limit,
            language)
        program_info = {
        "solution_id": solution_id,
        "problem_id": problem_id,
        "take_time": 0,
        "take_memory": 0,
        "pass_point":0,
        "user_id": user_id,
        "result": 0,
        }
        if ret == False:
            logging.error("no data%d.in problem_id:%d"%(i+1,problem_id))
            program_info['result']=result_code["System Error"]
            program_info['pass_point']=0
            program_info['take_time'],program_info['take_memory']=0,0
            return program_info
            
        if ret['result'] == 5:
            program_info['result'] = result_code["Runtime Error"]
            return program_info
        elif ret['result'] == 2:
            program_info['result'] = result_code["Time Limit Exceeded"]
            program_info['take_time'] = time_limit + 10
            return program_info
        elif ret['result'] == 3:
            program_info['result'] = result_code["Memory Limit Exceeded"]
            program_info['take_memory'] = mem_limit
            return program_info
        if max_time < ret["timeused"]:
            max_time = ret['timeused']
        if max_mem < ret['memoryused']:
            max_mem = ret['memoryused']
        result = judge_result(problem_id, solution_id, i + 1)
        if result == False:
            program_info['result']=result_code["System Error"]
            logging.error("compare data.out and user.out error\n")
            return program_info
        if result == "Wrong Answer" or result == "Output limit" or result == 'Presentation Error':
            program_info['result'] = result_code[result]
            break
        elif result == 'Accepted':
            program_info['result'] = result_code[result]
            program_info['pass_point']+=1
        else:
            logging.error("judge did not get result")
    program_info['take_time'] = max_time
    program_info['take_memory'] = max_mem
    return program_info

