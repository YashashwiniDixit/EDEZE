import json

from django.shortcuts import render, redirect
from utility_functions.date_functions import *
from utility_functions.db_functions import *

def aboutus(request):
    return render(request,'aboutus.html')

def contactUs(request):
    return render(request,'contactus.html')

def demo(request):
    return render(request,'demo.html')

def login(request):
    if request.session.has_key('user_id'):
        return checkIfLoggedIn(request)
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            con = DBConnection.getConnection()
            cur = con.cursor()
            query = "SELECT id,type FROM users WHERE username = %s AND password = %s;"
            cur.execute(query,(username,password))
            data = cur.fetchall()
            if len(data) == 1:
                request.session['user_id'] = data[0][0]

                if data[0][1] == 'admin':
                    return render(request,'adminIndex.html')
                elif data[0][1] == 'teacher':
                    query = "SELECT id FROM teachers WHERE user_id = %s;"
                    cur.execute(query, (data[0][0]))
                    data = cur.fetchall()
                    teacher_id = data[0][0]
                    request.session['teacher_id'] = teacher_id
                    courses = getTeacherCourses(teacher_id)
                    return render(request,'headerTeacher.html',{'courses':courses})
                elif data[0][1] == 'student':
                    query = "SELECT id FROM students WHERE user_id = %s;"
                    cur.execute(query, (data[0][0]))
                    data = cur.fetchall()
                    student_id = data[0][0]
                    request.session['student_id'] = student_id
                    courses = getStudentCourses(student_id)
                    return render(request,'studentIndex.html',{'courses':courses})
            return render(request,'e403.html')

    return render(request,'login.html')

def logout(request):
    if request.session.has_key('user_id'):
        del request.session['user_id']
        if request.session.has_key('teacher_id'):
            del request.session['teacher_id']
        elif request.session.has_key('student_id'):
            del request.session['student_id']
    return render(request,'login.html')


def progressAnalysis(request):
    student_id = request.session['student_id']
    con = DBConnection.getConnection()
    cur = con.cursor()
    print(student_id)
    query = "select date_time ,total_marks ,sum(marks) from exam e inner join questions_students qs on qs.exam_id = e.id where qs.student_id = %s group by qs.exam_id"
    cur.execute(query, (student_id))
    resultset = cur.fetchall()
    print(resultset)
    date_time = []
    score = []
    for r in resultset:
        date_time.append(r[0].strftime("%Y-%m-%d %H:%M:%S"))
        if(r[2]!=None):
            score.append(r[2]*100/r[1])
        else:
            score.append(0)
    date_time = json.dumps(date_time)
    score = json.dumps(score)
    print(date_time)
    print(score)
    query2="select name,sum(sum_marks),sum(total_marks) from ( select date_time ,total_marks ,sum(marks) as sum_marks,course_id from pariksha.exam as e inner join pariksha.questions_students as qs on qs.exam_id = e.id where qs.student_id = %s group by qs.exam_id ) as T inner join pariksha.course as c on T.course_id=c.id group by T.course_id"
    cur.execute(query2, (student_id))
    resultset2 = cur.fetchall()
    course_labels = []
    course_marks = []
    for r in resultset2:
        course_labels.append(r[0])
        course_marks.append(r[1]*100/float(r[2]))
    course_labels = json.dumps(course_labels)
    course_marks = json.dumps(course_marks)
    print(course_labels)
    print(course_marks)
    return render(request,'progressAnalysis.html',{'date_time':date_time, 'score':score,'course_labels':course_labels,'course_marks':course_marks})

def analyticsForTeacher(request,course_id):
    if request.session.has_key('teacher_id'):
        course = getCourse(course_id)
        print(course)
        con = DBConnection.getConnection()
        cur = con.cursor()
        query1 = "SELECT course_id,count(student_id) FROM pariksha.course_students where course_id=%s;"
        cur.execute(query1, (course_id))
        student_count = cur.fetchall()
        print(student_count)
        query2 = "SELECT course_id,id,date_time FROM pariksha.exam where course_id=%s;"
        cur.execute(query2, (course_id))
        exam_timeline = cur.fetchall()
        exam_labels = []
        exam_time = []
        for e in exam_timeline:
            exam_labels.append(1)
            exam_time.append(e[2].strftime("%Y-%m-%d %H:%M:%S"))
        exam_labels = json.dumps(exam_labels)
        exam_time = json.dumps(exam_time)
        print(exam_labels)
        print(exam_time)
        query3 = "SELECT course_id,id, start_date_time FROM pariksha.assignment where course_id=%s;"
        cur.execute(query3, (course_id))
        assignment_timeline = cur.fetchall()
        assignment_labels = []
        assignment_time = []
        for a in assignment_timeline:
            assignment_labels.append(1)
            assignment_time.append(a[2].strftime("%Y-%m-%d %H:%M:%S"))
        assignment_labels = json.dumps(assignment_labels)
        assignment_time = json.dumps(assignment_time)
        print(assignment_labels)
        print(assignment_time)
        query4 = "select exam_id,title, sum(marks) as marks, total_marks from pariksha.questions_students as qs inner join pariksha.exam as e on qs.exam_id=e.id where course_id=%s group by qs.exam_id;"
        cur.execute(query4, (course_id))
        exam_marks = cur.fetchall()
        exam_labels = []
        exam_percentage = []
        for e in exam_marks:
            exam_labels.append(e[1])
            if(e[2]!=None):
                exam_percentage.append(e[2]*100/(float(e[3])*(student_count[0][1])))
            else:
                exam_percentage.append(0)
            
        exam_labels = json.dumps(exam_labels)
        exam_percentage = json.dumps(exam_percentage)
        print(exam_labels)
        print(exam_percentage)
    return render(request, 'AnalyticsForTeacher.html',{'exam_labels':exam_labels,'exam_time':exam_time,'assignment_labels':assignment_labels,'assignment_time':assignment_time})

def viewAnalysis(request,exam_id):
    student_id = request.session['student_id']
    con = DBConnection.getConnection()
    cur = con.cursor()
    query = "select sum(knowledge_marks),sum(grammar_marks),knowledge_ratio,grammar_ratio,total_marks from questions_students qs inner join exam on exam.id = qs.exam_id where exam_id = %s and student_id = %s"
    cur.execute(query,(5,student_id))
    KG_marks = cur.fetchone()
    print(KG_marks)
    km = KG_marks[0]/(KG_marks[2]*KG_marks[4])
    gm = KG_marks[1]/(KG_marks[3]*KG_marks[4])
    temp = []
    temp.append(km)
    temp.append(gm)
    KG_marks = json.dumps(list(temp))
    query1 = "select qs.marks,q.marks,course_outcome from questions q inner join questions_students qs on q.id = qs.question_id where qs.exam_id = %s and student_id = %s and qs.marks is not NULL"
    cur.execute(query1, (exam_id, student_id))
    course_out_ratio = cur.fetchall()
    print(course_out_ratio)
    co = []
    mks = []
    for i in course_out_ratio:
        co.append(i[2])
        mks.append((i[0]/i[1])*100)
    c_out = json.dumps(co)
    mks_out = json.dumps(mks)
    return render(request, 'viewAnalysis.html',{'KG_marks':KG_marks,'c_out':c_out,'mks_out':mks_out})




def index(request):
    return render(request,'headerGeneral.html')