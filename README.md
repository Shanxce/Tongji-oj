# Tongji-oj
同济大学2019级计算机科学与技术，计算机科学导论课程网页制作大作业，同济oj

## 项目简介
* **类型**: 一个在线评测代码的网站，能够评测c++、c、python代码。可以实现添加题目来扩充题库，每道题还有论坛部分，为大家提供一个交流问题的场所。
* **前端实现**：使用了html、css、js传统三件套，自主设计与实现。
* **后端实现**：借助了python中的flask模块实现后端对前端的渲染。
* **数据库**：考虑到轻量化的实现，使用了python的sqlite实现数据存储。
<hr>

## 项目动机与设计思路
* **原同济OJ**：缺乏动效，界面单调，缺少色彩和美术，同学需要对题目进行讨论却无法实现，缺少相关版面
* **重写OJ**：设计网站美术，设计大致框架，增加网站界面动效，增加错误提示信息
* **讨论版（论坛）**：问题新增讨论，个人题问，个人回答解决问题，部分代码思路分享，论坛发帖全员共同参与讨论
<hr>

## 项目实现功能

#### OJ部分
* **提交代码**：可以在问题界面查找具体问题，查看问题介绍以及样例，在代码提交界面提交代码，网站使用后端存储的输入输出数据，自动比对后返回评测结果，目前有的返回值有：

显示结果|详细说明
--|:--
AC|输出正确
WA|输出错误
TLE|运行超时
MLE|内存超限
RE|段错误
CE|编译错误

* **发布新问题**：管理员可以发布新的问题，提交问题介绍、样例输入输出、测评输入输出文件，就可以让其他人尝试解决该问题。
* **查看状态**：查看所有问题提交的状态
* **查看个人信息**：查看个人头像、昵称、邮件，同时可以查看自己已经尝试过的问题以及自己的提问（论坛模块）

#### 论坛部分
* **查看问题**：可以看到当前问题的所有提问，在首页仅显示问题的题目，点击后展开并显示题目的回复；点击展开所有回答，可以跳转到问题的主页
* **发布与删除回复**：在每个问题的主页，可以对问题进行回复；每个人可以删除自己的回复
* **发布问题**：每个人可以就当前题目发布问题，等待其他同学或老师的回复
<hr>

## 前后端开发

#### 评测机关键技术
OJ网站的灵魂在评测机，既要精确检测出使用了多少内存和时间以检查是否满足时空限制，又要防止恶意代码破坏服务器——这涉及到安全问题。此外为了与数据库交互还需要将评测机封装为python模块以方便调用。
* **CPython封装**：CPython库是一个可以将C语言编译成为Python模块的库。通过限定输入输出格式，注册函数等操作将评测机的接口封装成Python模块。之后便可以像调用普通Python库一样使用评测机。
* **资源限制和检测**：在Linux系统中提供了一系列API以监测和限定资源。通过父进程fork子进程并使用setrlimit对子进程的时间、空间、堆栈等资源进行限制，当子进程超出限制就会被杀死，然后用wait4就可以获取子进程的CPU占用等信息以核查是否满足时空要求。
* **安全保护**：用Linux系统提供的代码注入技术，监视被评测程序与内核交互部分，例如系统调用，内核向进程发出的信号，调用文件等等信息，如果调用了可能危害系统的函数、或访问了不该访问的文件，父进程会向子进程发出SIGKILL信号，子进程就会被杀死。

#### 后端开发
* **登录**：登录的后端使用了flask_login，将前端表单输入的内容与数据库中存储的信息进行比对，如果比对到正确的信息，则将用户信息在User类中记录，供随后的前后端进行访问
* **注册验证码**：为了保证注册的安全性，我们通过flask_mail模块设置了邮箱验证码，可向用户提供的邮箱中发送验证码，并将用户填入的验证码与发送的验证码进行比对，当比对正确时用户才能进行注册，将注册信息写进数据库
* **数据库**：为了更好的完成OJ功能，我们使用了sqlite3模块来建立数据库，建立了用户信息、OJ题目、论坛提问、论坛回答等6张表，更好地对网站信息进行管理
* **代码重构**：在完成OJ功能后，我们使用blueprint对代码进行了重构，将完成同一功能的代码放在一起进行管理，使项目的可维护性提高、代码的可读性提高

#### 前端开发
* **传统三件套的结合**：在整个网站的设计中，自主设计了网站的架构，通过合理的使用、结合传统三件套（html、css、javascript），制作出了界面精美、功能精良的网站前端
* **框架的使用**：部分位置使用了bootstrap的框架模板，让前端界面看起来更加整洁，适配性更好
* **javascript模板的使用**：使用了一些javascript的功能，比如canvas、看板娘等，让界面不再单调，同学们在做题之余也能有一些休闲

<hr>

## 成员分工

姓名|学号|任务
--|:--:|:--:
彭瀚|1853568|整体数据库构建以及功能整合
孔庆晨|1853047|登录注册部分前端部分
夏文勇|1851506|论坛功能前端页面部分
金唱|1854082|论坛功能后端部分以及前后端连接
汪冰海|1854094|OJ功能代码评测机部分
方润楠|1951568|OJ功能后端部分以及前后端连接
张馨月|1952339|OJ功能前端页面部分
<hr>

## 部分界面与功能展示
#### 登录界面
[![rs87OH.png](https://s3.ax1x.com/2020/12/22/rs87OH.png)](https://imgchr.com/i/rs87OH)

#### 主页
[![rsGi0s.png](https://s3.ax1x.com/2020/12/22/rsGi0s.png)](https://imgchr.com/i/rsGi0s)
#### OJ问题查看
[![rs8fFx.png](https://s3.ax1x.com/2020/12/22/rs8fFx.png)](https://imgchr.com/i/rs8fFx)
#### 提交问题状态
[![rs8RT1.png](https://s3.ax1x.com/2020/12/22/rs8RT1.png)](https://imgchr.com/i/rs8RT1)
#### 问题详情
[![rs8olD.png](https://s3.ax1x.com/2020/12/22/rs8olD.png)](https://imgchr.com/i/rs8olD)
#### 提交新问题
[![rs8hY6.png](https://s3.ax1x.com/2020/12/22/rs8hY6.png)](https://imgchr.com/i/rs8hY6)
#### 问题讨论区（论坛）
[![rs8zp8.png](https://s3.ax1x.com/2020/12/22/rs8zp8.png)](https://imgchr.com/i/rs8zp8)
#### 搜索问题
[![rsG9XQ.png](https://s3.ax1x.com/2020/12/22/rsG9XQ.png)](https://imgchr.com/i/rsG9XQ)
#### 点击问题查看热门回复
[![rs8vff.png](https://s3.ax1x.com/2020/12/22/rs8vff.png)](https://imgchr.com/i/rs8vff)
#### 查看全部回复
[![rsGPmj.png](https://s3.ax1x.com/2020/12/22/rsGPmj.png)](https://imgchr.com/i/rsGPmj)
#### 回复问题
[![rs84fK.png](https://s3.ax1x.com/2020/12/22/rs84fK.png)](https://imgchr.com/i/rs84fK)
#### 回复成功，此时可以删除自己的回复
[![rs8jtP.png](https://s3.ax1x.com/2020/12/22/rs8jtP.png)](https://imgchr.com/i/rs8jtP)
#### 提交讨论问题
[![rs8Xkt.png](https://s3.ax1x.com/2020/12/22/rs8Xkt.png)](https://imgchr.com/i/rs8Xkt)
<hr>

## 项目进度

时间|实现内容
--|:--:
2020-11-22 19:00|讨论网页的功能实现，给出3个备选方案
2020-11-25 22:30|确定网页主题：OJ平台+论坛
2020-11-26 21:30|划分具体子任务
2020-11-27 23:00|每个人根据喜好、特点选择子任务
2020-11-29 12:00|各部分前端设计完成
2020-12-2 17:00|各部分数据库设计完成
2020-12-12 13:00|登录注册界面前端完成
2020-12-12 21:00|OJ部分前端完成
2020-12-13 19:00|论坛部分前端完成
2020-12-15 18:00|数据库部分完成
2020-12-15 23:00|论坛部分前后端调试成功
2020-12-15 22:00|登录注册界面前后端调试成功
2020-12-20 17:00|OJ部分前后端调试成功
2020-12-21 13:00|功能整合完成
2020-12-21 21:00|修复BUG
<hr>





[url=https://imgchr.com/i/rs8olD][img]https://s3.ax1x.com/2020/12/22/rs8olD.png[/img][/url]
[url=https://imgchr.com/i/rs8fFx][img]https://s3.ax1x.com/2020/12/22/rs8fFx.png[/img][/url]
[url=https://imgchr.com/i/rs8hY6][img]https://s3.ax1x.com/2020/12/22/rs8hY6.png[/img][/url]
[url=https://imgchr.com/i/rs8RT1][img]https://s3.ax1x.com/2020/12/22/rs8RT1.png[/img][/url]
[url=https://imgchr.com/i/rs87OH][img]https://s3.ax1x.com/2020/12/22/rs87OH.png[/img][/url]
[url=https://imgchr.com/i/rs8vff][img]https://s3.ax1x.com/2020/12/22/rs8vff.png[/img][/url]
[url=https://imgchr.com/i/rs8Xkt][img]https://s3.ax1x.com/2020/12/22/rs8Xkt.png[/img][/url]
[url=https://imgchr.com/i/rs84fK][img]https://s3.ax1x.com/2020/12/22/rs84fK.png[/img][/url]
[url=https://imgchr.com/i/rs8jtP][img]https://s3.ax1x.com/2020/12/22/rs8jtP.png[/img][/url]
[url=https://imgchr.com/i/rs8zp8][img]https://s3.ax1x.com/2020/12/22/rs8zp8.png[/img][/url]
[url=https://imgchr.com/i/rsG9XQ][img]https://s3.ax1x.com/2020/12/22/rsG9XQ.png[/img][/url]
[url=https://imgchr.com/i/rsGPmj][img]https://s3.ax1x.com/2020/12/22/rsGPmj.png[/img][/url]
[url=https://imgchr.com/i/rsGi0s][img]https://s3.ax1x.com/2020/12/22/rsGi0s.png[/img][/url]
<!-- 
```flow
st=>start: 开始
op=>operation: My Operation
cond=>condition: Yes or No?
e=>end
st->op->cond
cond(yes)->e
cond(no)->op
&``` -->
