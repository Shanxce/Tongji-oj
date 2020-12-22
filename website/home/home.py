from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import current_user, logout_user, login_required
import sqlite3 as sql
from datetime import datetime
import os
from website.home import home_bp
from website import basedir

@home_bp.route("/home/")
@login_required
def home():
    return render_template('ojhome.html')

@home_bp.route("/about/")
@login_required
def ShowUserPage():
    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()

    #查找提过的问题
    cur.execute("SELECT * FROM Questions WHERE question_creator_id = ?", (current_user.id, ))
    con.commit()
    user_questions = cur.fetchall()
    col_name_questions = [tuple[0] for tuple in cur.description]
    user_questions_dic = list(dict(zip(col_name_questions, i)) for i in user_questions)
    jump_url_questions = ['/problem/forum/' + str(user_questions_dic[i]["problem_id"]) + '/' + str(user_questions_dic[i]["question_id"]) + '/' \
        for i in range(len(user_questions_dic))]
    jump_url_delete = ['/problem/forum/' + str(user_questions_dic[i]["problem_id"]) + '/' + str(user_questions_dic[i]["question_id"]) + '/delete/' \
        for i in range(len(user_questions_dic))]

    #查找交过的题
    cur.execute("SELECT a.* FROM Solutions a inner join(select user_id, problem_id, max(submit_time) submit_time FROM Solutions WHERE user_id = ? GROUP BY problem_id)\
        b ON a.problem_id = b.problem_id AND a.user_id = b.user_id AND a.submit_time = b.submit_time ORDER BY problem_id", (current_user.id, ))
    con.commit()
    user_solutions = cur.fetchall()
    col_name_solutions = [tuple[0] for tuple in cur.description]
    user_solutions_dic = list(dict(zip(col_name_solutions, i)) for i in user_solutions)
    jump_url_problems = ['/problem/' + str(user_solutions_dic[i]["problem_id"]) + '/' for i in range(len(user_solutions_dic))]

    cur.close()
    con.close()
    return render_template("About.html", questions = list(zip(user_questions_dic, jump_url_questions, jump_url_delete)), \
        submitted_problems = list(zip(user_solutions_dic, jump_url_problems, [i for i in range(len(jump_url_problems))])))


@home_bp.route('/problem/')
@login_required
def problem():
    conn = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db"))
    cur = conn.cursor()
    conn.row_factory = sql.Row
    cur.execute('select problem_name,problem_id from OJProblems')
    rows=cur.fetchall()
    for row in rows:
        print(row[1])
    conn.commit()
    cur.close()
    conn.close()
    return render_template('problem.html',rows=rows)


@home_bp.route("/status/")
@login_required
def Status():
    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()
    cur.execute("SELECT * FROM Solutions ORDER BY submit_time DESC")
    con.commit()
    submit_record = cur.fetchall()[0: 10]
    col_name_submit = [tuple[0] for tuple in cur.description]
    submit_record_dic = list(dict(zip(col_name_submit, i)) for i in submit_record)
    #jump_url_problems = ['/problem/' + str(submit_record_dic[i]["problem_id"] + '/' for i in range(len(submit_record_dic)))]
    color = {
        "AC": "background-color: rgb(19, 251, 54);",
        "WA": "background-color: #f05654;",
        "TLE": "background-color: #ab82ff;",
        "MLE": "background-color: #97ffff;",
        "CE": "background-color: #ffc0cb;",
        "PE": "background-color: #b0e0e6;",
        "RE": "background-color: #ff8c00;",
        "SE": "background-color: #8fbc8f;",
        "waiting": "background-color: #d3d3d3;"
    }
    bg_color = [color[sub["judge_state"]] for sub in submit_record_dic]
    con.commit()
    cur.close()
    con.close()
    return render_template("status.html", rows = list(zip(submit_record_dic,bg_color)))


@home_bp.route('/add_pro/')
@login_required
def problem_add():  
    return render_template('inner.html')


@home_bp.route('/added_pro/',methods=['GET', 'POST'])
@login_required
def problem_added():
    if request.method == 'POST':
        conn = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db"))
        cur = conn.cursor()
        conn.row_factory = sql.Row
        cur.execute("select count (*) from OJProblems")
        rows=cur.fetchall()
        problem_id=int(rows[0][0])+1001
        result=request.form
        problem_name = result["problem_name"]
        time_limit = result["time_limit"]
        memory_limit = result["memory_limit"]
        description = result['description']
        sample_in = request.files['sample_in']
        sample_out = request.files['sample_out']
        data_in =request.files['data_in']
        date_out=request.files['date_out']
        path = f'{basedir}/static/problem/{problem_id}'
        if not os.path.exists(path):
            os.mkdir(path)
            os.mkdir(f'{path}/sample')
            os.mkdir(f'{path}/test_data')
        sample_in.save(f'{path}/sample/{problem_id}_sample_in.png')
        sample_in_addr=f'{path}/sample/{problem_id}_sample_in.png'
        sample_out.save(f'{path}/sample/{problem_id}_sample_out.png')
        sample_out_addr=f'{path}/sample/{problem_id}_sample_out.png'
        data_in.save(f'{path}/test_data/data1.in')
        data_in_addr=f'{path}/test_data/data1.in'
        date_out.save(f'{path}/test_data/data1.out')
        data_out_addr=f'{path}/test_data/data1.out'
        cur.execute("insert into OJProblems values(?,?,?,?,?,?,?,?,?,?,?)",(sample_in_addr,sample_out_addr,10,0,description,problem_id,problem_name,data_in_addr,data_out_addr,time_limit,memory_limit))        
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('home.problem'))
