from . import config
import os
def check_dangerous_code(solution_id, language):
    realpath = os.path.join(config.work_dir, str(solution_id))
    filename = {
        'python3': "main.py",
        'g++': "main.cpp",
        'gcc':"main.c",
    }
    realpath = os.path.join(realpath, filename[str(language)])
    if language in ['python2', 'python3']:
        code=open(realpath,'r').readlines()
        support_modules = [
            're',  # 正则表达式
            'sys',  # sys.stdin
            'string',  # 字符串处理
            'scanf',  # 格式化输入
            'math',  # 数学库
            'cmath',  # 复数数学库
            'decimal',  # 数学库，浮点数
            'numbers',  # 抽象基类
            'fractions',  # 有理数
            'random',  # 随机数
            'itertools',  # 迭代函数
            'functools',
            #Higher order functions and operations on callable objects
            'operator',  # 函数操作
            'readline',  # 读文件
            'json',  # 解析json
            'array',  # 数组
            'sets',  # 集合
            'queue',  # 队列
            'types',  # 判断类型
        ]
        for line in code:
            if line.find('import') >= 0:
                words = line.split()
                tag = 0
                for w in words:
                    if w in support_modules:
                        tag = 1
                        break
                if tag == 0:
                    return False
        return True
    if language in ['gcc', 'g++']:
        code = open(realpath, 'r').read()
        if code.find('system')!=-1:
            return False
        return True

