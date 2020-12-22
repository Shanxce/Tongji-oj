# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_login import current_user, logout_user, login_required
import sqlite3 as sql
from datetime import datetime
import os
from website.forum import forum_bp


@forum_bp.route('/problem/forum/<int:problem_id>/', methods = ['GET'])  #进入讨论区，显示数据库中的问�?
@login_required
def display(problem_id):
    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()
    cur.execute("select * from Questions WHERE problem_id = ?", (problem_id, ))
    con.commit()
    questions = cur.fetchall()  #读到的数据库的列表（两层�?
    col_name_questions = [tuple[0] for tuple in cur.description]
    questions_dic = list(dict(zip(col_name_questions, i)) for i in questions) #把数据库列表的内层变为字�?
    question_creators_id = list(questions_dic[i]['question_creator_id'] for i in range(len(questions_dic)))
    jump_url_questions = [str(questions_dic[i]["question_id"]) for i in range(len(questions))]

    question_creators_pic = []
    question_creators_name = []
    for i in range(len(question_creators_id)):
        cur.execute("select * from UserInfo where user_id = ?", (question_creators_id[i], ))
        con.commit()
        question_creators = cur.fetchone()
        col_name_creators = [tuple[0] for tuple in cur.description]
        question_creators_dic = dict(zip(col_name_creators, question_creators))
        question_creators_pic.append(question_creators_dic['user_head'])
        question_creators_name.append(question_creators_dic['user_name'])
    question_creators_info = list(zip(question_creators_name, question_creators_pic))

    answer_per_questions = []         #大列表，内层是每一个question的列表，每一个question列表内是每一个回答的字典
    question_ids = list(questions_dic[i]['question_id'] for i in range(len(questions_dic)))
    for i in range(len(question_ids)):
        cur.execute("select * from Answers where question_id = ?", (question_ids[i], ))
        con.commit()
        answers = cur.fetchall()
        col_name_answers = [tuple[0] for tuple in cur.description]
        answers_dic = list(dict(zip(col_name_answers, i)) for i in answers) #对于某一个问题的所有回答列表，列表里每一个回答有一个dict存放信息
        answer_per_questions.append(answers_dic)
    
    con.close()
    return render_template("home.html", alldata = list(zip(questions_dic, question_creators_info, answer_per_questions, jump_url_questions)),\
         back_home_url = "./")
    # 这里questions是传过去的列表，里面是所有的问题即问题相关信息；jump_url是按按钮要跳转的页面�?
    # home.html里显示传过去的问题，如果点击具体问题，则跳转到下一个全部回答页�?


@forum_bp.route('/problem/forum/<int:problem_id>/<int:question_id>/')
@login_required
def ShowAnswerPage(problem_id, question_id):
    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()
    cur.execute("select * from Answers WHERE question_id = ?", (question_id, ))
    con.commit()
    answers = cur.fetchall()  #读到的数据库的列表（两层�?
    col_name_answers = [tuple[0] for tuple in cur.description]
    answers_dic = list(dict(zip(col_name_answers, i)) for i in answers)  #把数据库列表的内层变为字�?
    #answer_len = len(answers)

    answer_creators_info = []    #一个大列表，里面有很多字典，一个字典是一个answer的创建者信�?
    for i in range(len(answers)):
        cur.execute("select * from UserInfo where user_id = ?", (answers_dic[i]["answerer_id"], ))
        con.commit()
        answer_creator_info = cur.fetchone()    #一个问题的回答者信�? 
        col_name_creator = [tuple[0] for tuple in cur.description]
        answer_creator_dic = dict(zip(col_name_creator, answer_creator_info))
        answer_creators_info.append(answer_creator_dic)
    #print(answer_creators_info)

    cur.execute("select * from Questions WHERE question_id = ?", (question_id, ))
    con.commit()
    question = list(cur.fetchone())    #查看进入的回答所隶属的问�?
    pageviews = question[-1]
    cur.execute("update Questions SET pageview = ? WHERE question_id = ?", (pageviews + 1, question_id))  #改变数据库中浏览�?
    con.commit()

    cur.execute("select * from Questions WHERE question_id = ?", (question_id, ))  #改变数据库内容后重新�?
    con.commit()
    question = list(cur.fetchone())
    col_name_question = [tuple[0] for tuple in cur.description]
    question_dic = dict(zip(col_name_question, question))    #该问题的字典，需要传给前端在网页顶部显示问题及浏览量
    question_creator_id = question_dic["question_creator_id"]
    #print(question_creator_id)

    cur.execute("select * from UserInfo where user_id = ?", (question_creator_id, ))
    con.commit()
    question_creator = cur.fetchone()
    col_name_creator = [tuple[0] for tuple in cur.description]
    question_creator_info = dict(zip(col_name_creator, question_creator))   #提问用户的信息字�?
    #print(question_creator_info)

    jump_url_delete = [str(answers_dic[i]["answer_id"]) + "/delete/" for i in range(len(answers))]
    con.close()
    return render_template("respond.html", answers_info = list(zip(answers_dic, answer_creators_info, jump_url_delete)), \
        question_info = (question_dic, question_creator_info), back_home_url = "..")
    #这个模板里面有填入自己的回答的填空矿，如果填入，则填入的结果连接到submitresult的url


@forum_bp.route('/problem/forum/<int:problem_id>/submit/')
@login_required
def SubmitQuestions(problem_id):
    return render_template("submit_questions.html")   
    #这个模板里面填入的结果连接到submitresult的url


@forum_bp.route('/problem/forum/<int:problem_id>/submitresult/', methods = ['POST'])  
@login_required
def SubmitQuestionsResult(problem_id):
    question_title = request.form['submit_title']  #填进去的提问标题
    question_text = request.form['submit_text']  #填进去的提问内容
    '''question_pic = request.files['pic']   #上传的图�?'''
    #creator_id = request.cookies.get("user_name")  #cookies得到用户�?
    creator_id = current_user.id
    
    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()
    cur.execute("insert into Questions values(NULL, ?, ?, ?, ?, ?, ?, ?)", (question_title, problem_id, question_text, None, creator_id, \
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0))
    con.commit()
    con.close()
    #连接数据库并将内容写进数据库，但是文件和图片地址暂时传NULL
    # cur.execute("select count(*) from Questions")  #读取刚刚存入的question的id
    # con.commit()
    # count = cur.fetchone() - 1
    # question_text_address = 'questions/' + 'problem' + str(problem_id) + '/' + 'question' + str(count) + 'text.txt'
    # with open(question_text_address, "w") as f:   #创建文件路径并将内容写进文件
    #     f.write(question_text)
    #     f.close()
    # question_pic_address = 'questions/' + 'problem' + str(problem_id) + '/' + 'question' + str(count)
    # question_pic.save(os.path.join(app.config[question_pic_address], secure_filename(question_pic.filename)))  #创建图片路径并保存图�?
    # cur.execute("update Questions SET question_text_address = ? WHERE question_id = ?", (question_text_address, count))
    # con.commit()
    # cur.execute("update Questions SET question_pic_address = ? WHERE question_id = ?", (question_pic_address, count))
    # con.commit()
    # #更新表中文件和图片地址
    
    return redirect(url_for('forum.display', problem_id = problem_id))  #返回这个problem的question列表


@forum_bp.route('/problem/forum/<int:problem_id>/<int:question_id>/delete/', methods = ['POST', 'GET'])  #进入讨论区，显示数据库中的问题?
@login_required
def QuestionDelete(problem_id, question_id):
    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()
    cur.execute("DELETE FROM Questions WHERE question_id = ?", (question_id, ))
    con.commit()

    cur.execute("DELETE FROM Answers WHERE question_id = ?", (question_id, ))
    con.commit()
    con.close()
    return redirect(url_for('forum.display', problem_id = problem_id))


@forum_bp.route('/problem/forum/<int:problem_id>/<int:question_id>/<int:answer_id>/delete/', methods = ['POST', 'GET'])  #进入讨论区，显示数据库中的问题?
@login_required
def AnswerDelete(problem_id, question_id, answer_id):
    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()
    cur.execute("delete from Answers where answer_id = ?", (answer_id, ))
    con.commit()
    con.close()
    return redirect(url_for('forum.ShowAnswerPage', problem_id = problem_id, question_id = question_id))


#@app.route('/problem/forum/<problem_id>/<question_id>/submit')
#def SubmitAnswers(problem_id, question_id):
#    return render_template("submit_answer.html", jump_url = '/problem/forum/' + str(problem_id) + '/' + str(question_id) + '/submitresult')   
    #这个模板里面填入的结果连接到submitresult的url


@login_required
@forum_bp.route('/problem/forum/<int:problem_id>/<int:question_id>/submitresult/', methods = ['POST'])
def SubmitAnswersResult(problem_id, question_id):
    answer_text = request.form['reply_submit']  #填进去的回答内容
    #answer_pic = request.files['pic']   #上传的图�?
    #creator_id = request.cookies.get("user_name")  #cookies得到用户�?
    creator_id = current_user.id
    
    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()
    cur.execute("insert into Answers values(NULL, ?, ?, ?, ?, ?)", (answer_text, None, question_id, creator_id, \
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    con.commit()
    #连接数据库并将内容写进数据库
    # cur.execute("select count(*) from Answers")  #读取刚刚存入的answer的id
    # con.commit()
    # count = cur.fetchone() - 1
    # answer_text_address = 'answers/' + 'question' + str(question_id) + '/' + 'answer' + str(count) + 'text.txt'
    # with open(answer_text_address, "w") as f:   #创建文件路径并将内容写进文件
    #     f.write(answer_text)
    #     f.close()
    # answer_pic_address = 'answers/' + 'question' + str(question_id) + '/' + 'answer' + str(count)
    # answer_pic.save(os.path.join(app.config[answer_pic_address], secure_filename(answer_pic.filename)))  #创建图片路径并保存图�?
    # cur.execute("update Questions SET answer_text_address = ? WHERE answer_id = ?", (answer_text_address, count))
    # con.commit()
    # cur.execute("update Questions SET answer_pic_address = ? WHERE answer_id = ?", (answer_pic_address, count))
    # con.commit()
    # #更新表中文件和图片地址
    
    con.close()
    return redirect(url_for('forum.ShowAnswerPage', problem_id = problem_id, question_id = question_id))


@login_required
@forum_bp.route("/users/<int:user_id>/questions/")
def ShowUserQuestions(user_id):
    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()
    cur.execute("select * from questions WHERE creator_id = ?", user_id)
    con.commit()
    user_questions = cur.fetchall()
    col_name_questions = [tuple[0] for tuple in cur.description]
    user_questions_dic = list(dict(zip(col_name_questions, i)) for i in user_questions)  #把数据库列表的内层变为字�?
    jump_url = ["/problem/forum/" + str(user_questions_dic[i]["problem_id"]) \
         + '/' + str(user_questions_dic[i]["question_id"]) + '/0' for i in range(len(user_questions))]
    #如果点击问题，则到达问题下全部回答界�?
    con.close()
    return render_template("user_question.html", user_questions = user_questions_dic, jump_url = jump_url)


@login_required
@forum_bp.route('/problem/forum/<int:problem_id>/search', methods=['POST'])
def SearchQuestion(problem_id):
    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()
    search_string = request.form["search_input"]
    cur.execute("select * from Questions WHERE problem_id = ? AND question_title LIKE ?", (problem_id, "%"+search_string+"%"))
    con.commit()
    questions = cur.fetchall()  #读到的数据库的列表（两层�?
    '''
    if quetions.empty():
        return render_template("home.html", alldata = list(zip(questions_dic, question_creators_info, answer_per_questions, jump_url_questions)))
    '''
    col_name_questions = [tuple[0] for tuple in cur.description]
    questions_dic = list(dict(zip(col_name_questions, i)) for i in questions) #把数据库列表的内层变为字�?
    question_creators_id = list(questions_dic[i]['question_creator_id'] for i in range(len(questions_dic)))
    jump_url_questions = [str(questions_dic[i]["question_id"]) for i in range(len(questions))]
    con.close()

    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()
    question_creators_pic = []
    question_creators_name = []
    for i in range(len(question_creators_id)):
        cur.execute("select * from UserInfo where user_id = ?", (int(question_creators_id[i]), ))
        con.commit()
        question_creators = cur.fetchone()
        col_name_creators = [tuple[0] for tuple in cur.description]
        question_creators_dic = dict(zip(col_name_creators, question_creators))
        question_creators_pic.append(question_creators_dic['user_head'])
        question_creators_name.append(question_creators_dic['user_name'])
    question_creators_info = list(zip(question_creators_name, question_creators_pic))

    answer_per_questions = []         #大列表，内层是每一个question的列表，每一个question列表内是每一个回答的字典
    question_ids = list(questions_dic[i]['question_id'] for i in range(len(questions_dic)))
    for i in range(len(question_ids)):
        cur.execute("select * from Answers where question_id = ?", (int(question_ids[i]), ))
        con.commit()
        answers = cur.fetchall()
        col_name_answers = [tuple[0] for tuple in cur.description]
        answers_dic = list(dict(zip(col_name_answers, i)) for i in answers) #对于某一个问题的所有回答列表，列表里每一个回答有一个dict存放信息
        answer_per_questions.append(answers_dic)
    
    con.close()
    return render_template("home.html", alldata = list(zip(questions_dic, question_creators_info, answer_per_questions, jump_url_questions)),\
         back_home_url = "./")
    # 这里questions是传过去的列表，里面是所有的问题即问题相关信息；jump_url是按按钮要跳转的页面�?
    # home.html里显示传过去的问题，如果点击具体问题，则跳转到下一个全部回答页�?

