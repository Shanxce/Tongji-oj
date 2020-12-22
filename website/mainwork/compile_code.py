from . import config
import os
import subprocess
import logging
def compile_code(solution_id, language):
    '''将程序编译成可执行文件'''
    dir_work = os.path.join(config.work_dir, str(solution_id))
    build_cmd = {
        "gcc":
        "gcc main.c -o main -Wall -lm -O2 -std=c99  -DONLINE_JUDGE",
        "g++": "g++ main.cpp -O2 -Wall -lm  -DONLINE_JUDGE -o main",
        "python3": 'python3 -m py_compile main.py',
    }
    print("language",language)
    if language not in build_cmd.keys():
        return False
    p = subprocess.Popen(
        build_cmd[str(language)],
        shell=True,
        cwd=dir_work,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = p.communicate()  # 获取编译错误信息
    print("out1:",out,err)
    out = str(out)
    err = str(err)
    print("out:",out,err)
    print(config.work_dir,solution_id)
    err_txt_path = os.path.join(config.work_dir, str(solution_id), 'error.txt')
    print("err_path",err_txt_path)
    f = open(err_txt_path, 'w')
    f.write(err)
    f.write(out)
    f.close()
    if p.returncode == 0:  # 返回值为0,编译成功
        return True
    logging.error("compile fail,solution_id:%d"%solution_id)
    #dblock.acquire()
    #update_compile_info(solution_id, err + out)  # 编译失败,更新题目的编译错误信息
    #dblock.release()
    return False



