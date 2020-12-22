import os
from flask import render_template, Flask, request, redirect, url_for
from flask_login import current_user
import sqlite3 as sql
from website.problem import problem_bp
from datetime import datetime
from flask_login import login_required
from website.mainwork.main import mainwork

basedir = os.path.dirname(os.path.abspath(__file__))


@problem_bp.route('/problem/<int:problem_id>/')
@login_required
def detail(problem_id):
    conn = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db"))
    cur = conn.cursor()
    conn.row_factory = sql.Row
    print(problem_id)

    cur.execute('select * from OJProblems where problem_id=%d'%(problem_id))
    rows=cur.fetchall()
    rows={
        "sample_in":rows[0][0],
        "sample_out":rows[0][1],        
        "task_cases":rows[0][2],
        "pass_person":rows[0][3],
        "problem_descripe":rows[0][4],
        "problem_id":rows[0][5],
        "problem_name":rows[0][6],
        "data_in":rows[0][7],
        "date_out":rows[0][8],
        "time_limit":rows[0][9],
        "room_limit":rows[0][10]
    }
    print(rows)
    conn.commit()
    cur.close()
    conn.close()
    return render_template('portfolio-details.html',rows=rows,pro_id=problem_id)

@problem_bp.route('/problem/<int:problem_id>/submit/')
@login_required
def submit(problem_id):
    conn = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db"))
    cur = conn.cursor()
    conn.row_factory = sql.Row
    cur.execute("select count (*) from Solutions")
    rows=cur.fetchall()
    solution_id=int(rows[0][0])+1
    print(solution_id)
    print(1)
    conn.commit()
    cur.close()
    conn.close()
    return render_template('submit.html',problem_id=problem_id,solution_id=solution_id)


@problem_bp.route('/problem/<int:problem_id>/submit/result/<int:solution_id>',methods = ['POST', 'GET'])
@login_required
def result(problem_id,solution_id):
    if(request.method=="POST"):
        result=request.form
    conn = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db"))
    cur = conn.cursor()
    conn.row_factory = sql.Row
    select=request.form.get('pro_lang')
    cur.execute("insert into Solutions values(?,?,?,?,?,?,?,?,?,?,?)",(solution_id,problem_id,select,current_user.id,result["message"],"f:/","waiting",30,100,100, \
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    cur.close()
    conn.close()
    #调用评测机器
    mainwork()
    conn = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db"))
    cur = conn.cursor()
    conn.row_factory = sql.Row
    cur.execute("select * from Solutions where solution_id=%d"%(solution_id))
    rows=cur.fetchall()
    for i in rows:
        print(i)
    row={
        "solution_id":rows[0][0],
        "problem_id":rows[0][1], 
        "pro_lang":rows[0][2],
        "user_id":rows[0][3],        
        "code_string":rows[0][4],
        "code_addr":rows[0][5],
        "judge_state":rows[0][6],
        "pass_case":rows[0][7],
        "time_used":rows[0][8],
        "memory_used":rows[0][9]
    }
    print(row)
    print(result["message"])
    color="#d8f635"
    if(row["judge_state"]=="AC"):
        color="#d8f635"
    else:
        if((row["judge_state"]=="WA")):
            color="#f05654"
        else:
            if(row["judge_state"]=="TLE"):
                color= "#ab82ff"
            else:
                if(row["judge_state"]=="MLE"):
                    color="#97ffff"
                else:
                    if(row["judge_state"]=="CE"):
                        color="#ffc0cb"
                    else:
                        if(row["judge_state"]=="PE"):
                            color="#b0e0e6"
                        else:
                            if(row["judge_state"]=="RE"):
                                color="#ff8c00"
                            else:
                                if(row["judge_state"]=="SE"):
                                    color="#8fbc8f"
                                else:
                                    color="#d3d3d3"
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('home.home'))

