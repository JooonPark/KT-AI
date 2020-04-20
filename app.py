import os
from flask import Flask
from flask import request , redirect

#'flask 이름은 아무거나 적어도 상관없다.'
memos = Flask(__name__, static_folder="static")

members =[
    {"id":"joon","pw":"1111"},
    {"id":"choi","pw":"2222"},
]
##################################################################
def get_menu():
    menu_temp = "<li><a href='/menu/{0}'>{0}</a></li>"
    menu = [e for e in os.listdir('content') if e[0] != '.']
    return "\n".join([menu_temp.format(m) for m in menu])

def get_template(filename):
    with open('workshop/'+filename, 'r', encoding = "utf-8") as f:
        template = f.read()

    return template

def get_menu1():
    menu_temp = "<li><a href='/menu1/{0}'>{0}</a></li>"
    menu = [e for e in os.listdir('content1') if e[0] != '.']
    return "\n".join([menu_temp.format(m) for m in menu])

def get_template1(filename):
    with open('workshop/'+filename, 'r', encoding = "utf-8") as f:
        template = f.read()

    return template
##################################################################
#메인 화면
@memos.route("/menu")
def index():
    id = request.args.get('id', '')
    template = get_template('memo-joon.html')
    
    title = id +'님 로그인 되었습니다.'
    content = '필요하신 항목을 선택해주세요.'
    menu = get_menu()
    return template.format(title,content,menu)

@memos.route("/menu1")
def index1():
    id = request.args.get('id', '')
    template = get_template1('memo-choi.html')
    
    title = id +'님 로그인 되었습니다.'
    content = '필요하신 항목을 선택해주세요.'
    menu = get_menu1()
    return template.format(title,content,menu)
#########################################################
#각 리스트들의 이름, 타이틀 만들기
@memos.route("/menu/<title>")
def make_title(title):
    template = get_template('memo-joon.html')
    
    with open(f"content/{title}", 'r') as f:
        content = f.read()
    
    menu = get_menu()
    return template.format(title,content,menu)

@memos.route("/menu1/<title>")
def make_title1(title):
    template = get_template1('memo-choi.html')
    
    with open(f"content1/{title}", 'r') as f:
        content = f.read()
    
    menu = get_menu1()
    return template.format(title,content,menu)

##################################################################

#list 삭제하기
@memos.route("/delete/<title>")
def delete(title):
    os.remove(f"content/{title}")
    return redirect('/menu')

@memos.route("/delete1/<title>")
def delete1(title):
    os.remove(f"content1/{title}")
    return redirect('/menu1')

########################################################################
#list 추가하기
@memos.route("/create", methods=['GET','POST'])
def create():
    template = get_template('create-joon.html')
    menu = get_menu()
    
    if request.method =='GET':
        return template.format('',menu)
    
    elif request.method == 'POST':
        
        with open(f"content/{request.form['title']}",'w') as f:
            f.write(request.form['desc'])
            
        return redirect('/menu')

@memos.route("/create1", methods=['GET','POST'])
def create1():
    template = get_template1('create-choi.html')
    menu = get_menu1()
    
    if request.method =='GET':
        return template.format('',menu)
    
    elif request.method == 'POST':
        
        with open(f"content1/{request.form['title']}",'w') as f:
            f.write(request.form['desc'])
            
        return redirect('/menu1')    
###########################################################################
#로그인 화면
@memos.route("/", methods=['GET','POST'])
def login():
    template = get_template('login.html')
    menu = get_menu()
    
    if request.method =='GET':
        return template.format("",menu)
    
    elif request.method == 'POST':
        
        #만약 회원이 아니라면, "회원이 아닙니다" 라고 알려주기
        m = [e for e in members if e['id'] == request.form['id']]
        if len(m) == 0:
             return template.format("회원이 아닙니다.")
            
        # 만약 패스워드가 다르면, "패스워드를 확인해 주세요"라고 알려주자
        if request.form['pw'] != m[0]['pw']:
            return template.format("패스워드를 확인해 주세요")
        
        if m[0]['id'] == 'joon':
            return redirect("/menu")
        else:
            return redirect("/menu1")