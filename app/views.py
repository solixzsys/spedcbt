"""
Definition of views.
"""
import app
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.registrationform import RegistrationForm
from app.models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.views import login,logout
from datetime import datetime
from django.http import JsonResponse
from django.core.cache import cache
def mylogin(request):
    matricno=request.POST.get('matricnumber','')
    request.session['matricno']=matricno
    #try:
    #    matric=Cbt_students.objects.get(matricnumber=matricno)
    #except Exception as e:
    #    return HttpResponseRedirect('/')


    return login(request,template_name='app/login.html',
            authentication_form=app.forms.BootstrapAuthenticationForm,
            extra_context={
                'title': 'Log in',
                'year': datetime.now().year,
                },
)


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
   
    return render(
        request,
        'app/index.html',
        {
           
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def register(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    print('**********inside view*************')
    if request.POST:
        form=RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            print('**********valid form*************')
            uname=form.cleaned_data['username']
            mnumber=form.cleaned_data['matricnumber']
            fname=form.cleaned_data['firstname']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            #form.cleaned_data['username']=fname+'_'+mnumber
            user=User.objects.create(username=fname+'_'+mnumber,email=email)
            user.set_password(password)
            user.save()
            print('***************user created***********')
           # up= Cbt_students(picture= request.FILES['id_picture'])
            print('picture.............', form.cleaned_data['picture'])
            form.save()
            return redirect('login')
        return render(
            request,
            'app/register.html',
       
            {
                'form':form,
                'title':'Student Registration Page',
                'year':datetime.now().year,
            
            }
        )
    else:     
        print('**********not valid form*************')
        form=RegistrationForm(initial={
            'level':Cbt_level.objects.all(),
            'session':Cbt_sessions.objects.all(),
            'semester':Cbt_semester.objects.all(),
            'faculty':Cbt_faculty.objects.all(),
            'department':Cbt_department.objects.all()
            })
        return render(
            request,
            'app/register.html',
       
            {
                'form':form,
                'title':'Student Registration Page',
                'year':datetime.now().year,
            
            }
        )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )
def boardpage(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    print(request.user)

    

    if request.user.is_authenticated():
        #u=User.objects.get(request.user.email)
        try:
            student=Cbt_students.objects.get(matricnumber= request.session['matricno'])
            if student.username != request.user.username:
                return HttpResponseRedirect('/login')
        except Exception as e:
            print(e)
            return HttpResponseRedirect('/login')

        email=request.user.email
        try:
            print('login email..............',email)
            s=Cbt_students.objects.get(email=email)
            #m=Cbt_modules.objects.all()
            schedule_exam = CBT_Exam.objects.all()
            m=schedule_exam
        


            return render(
                request,
                'app/boardpage.html',
                {
                    'title':'Boardpage',
                    'message':'Your board page.',
                    'year':datetime.now().year,
                    'student':s,
                    'modules':m
                }
            )
        except Exception as e:
            print('Error..............',e)
            return HttpResponseRedirect('/login/')
 
    return HttpResponseRedirect('/login/')

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


def result(request):
    if request.user.is_authenticated():
        try:
            std_session=Cbt_StudentSession.objects.filter(student__username__icontains=request.user)
            mod=std_session[0].module
            number_of_question=Cbt_questions.objects.filter(module=mod).count()
            print('mod from result ++++++++++++++++++++++++++',mod)

        except Exception as e:
            print('You have no Record Yet !!!')
            print(e)
            return HttpResponseRedirect('/')
        return render(request,'app/result.html',{
            'exam_info':std_session,
            'qnumber':number_of_question,
            })
    else:
        return HttpResponseRedirect('/login/')

def postanswer(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')



    data=request.GET.get('data',0)
    
    #qnum=request.GET.get('qnum',0)
    #if request.session.get('qnum',0)==0:
    #    request.session['qnum']=str(qnum)
    #else:
    #    request.session['qnum']=request.session['qnum']+"-"+str(qnum)    
    #    print('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy ',request.session.get('qnum'))
    #posting to examsession
    #parameters are:
    #user object
    #qkey from session
    #question object
    #studentchoice
    #result
    #questioncode
    user=request.user
    #print('user ',user,'  about to posted..................................')
    questionkey=request.session.get('qkey',0)
    #print('question key is ..........',questionkey)
    #print('data is...................',data)
    
    question=Cbt_questions.objects.get(pk=questionkey)
    studentchoice=data.strip('-')
   
    
    transchoice={0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'i'}
    print('transchoice[2]...................',transchoice[2])
    studentchoice=studentchoice.split('-')
    l1=""
    for choice in studentchoice:
        print('choice.........................',choice)
        if choice !='':
            l1=l1+transchoice[int(choice)]+'-'
    
    print('reconstructed choice....................................',l1.strip('-'))

    studentchoice=l1.strip('-')
    result=question.answer==studentchoice
    #print('answer is .......................',question.answer)
    if result:
        result=1
    else:
        result=0
    mn=request.session['matricno']
    std=Cbt_students.objects.get(matricnumber=mn)
    r=0
    a=0
    try:
        ques=Cbt_ExamSession.objects.get(question=question,student=std)
        ques.studentchoice=studentchoice
        ques.save()
        ques.result=result
        ques.save()
        print('updated...................................',ques)
        print('user ',user,'   updateed..................................')
        
    except Exception as e:
        print('Error update...............',e)
        
        Cbt_ExamSession.objects.create(student=std,question=question,studentchoice=studentchoice,result=result)

    request.session['tresult']=request.session.get('tresult',0)+result
    request.session['tattempt']=request.session.get('tattempt',0)+1
    #r=request.session['tresult']
    #a=request.session['tattempt']
        
    r=request.session.get('tresult',result)
    a=request.session.get('tattempt',1)
    #print('user ',user,'   posted..................................')
    #print('New created.............................................',ques)
    #restructiorint the student session model
    attempt_count=Cbt_ExamSession.objects.filter(student__matricnumber=mn,question__module__code=request.session['module']).count()
    x=Cbt_ExamSession.objects.filter(student__matricnumber=mn,question__module__code=request.session['module'])
    rt=0
    for i in x:
        rt=rt+i.result
    try:
        ss=Cbt_StudentSession.objects.get(student=std,module__code=request.session['module'])
        ss.total_score=rt
        ss.save()
        ss.total_attempt=attempt_count
        ss.save()
    except Exception as e:
        ss=Cbt_StudentSession.objects.create(student=std,module=Cbt_modules.objects.get(code=request.session['module']),exam_status='STARTED',date=datetime.utcnow(),total_score=rt,total_attempt=attempt_count)
        print(std.username, ' Created.............................................................')
    #try:
    #    print('updating .............................................',std.username)
    #    ss=Cbt_StudentSession.objects.get(student=std)
    #    ss.total_score=r
    #    ss.save()
    #    ss.total_attempt=a
    #    ss.save()
    #except Exception as e:
    #    print(std.username,' not found...................................')
    #    print(e)
    #    ss=Cbt_StudentSession.objects.create(student=std,module=Cbt_modules.objects.get(code=request.session['module']),exam_status='STARTED',date=datetime.utcnow(),total_score=r,total_attempt=a)
    #    print(std.username, ' Created.............................................................')
    #updating the Cbt_STUDENTSESSION Table
    


   



    return JsonResponse({
        #'data':list(set(list(request.session.get('qnum').split('-'))))
        'data':''
        })


def reset(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    print('inside reset...............................................')
    #if request.session.has_key('module'):
    #    del request.session['module']
    #    del request.session['pagenum']
    #    del request.session['sessionstarted']
    #    del request.session['ques']
    #    del request.session['candidate']
    #    del request.session['questioncode']
    #    del request.session['qkey']
    #    del request.session['matricno']
    #    del request.session['tattempt']
    #    del request.session['tresult']
    #    print('session deleted.........................')
    request.session.flush()
    logout(request)
    return HttpResponseRedirect('/boardpage/')




def questionpage1(request,module):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated():
        if request.session.get('sessionstart',0)==1:

            print('sessionstart is set ............')
        else:
            print('sessionstart is not set ............')
        print(module ," selected..............")
        #print(" page..............",page )
        
        step=0

        if module=='prev':
            module=request.session['module']
            step=-1
        if module=='next':
            module=request.session['module']
        if  (request.session.get('sessionstart',0) != 1):
            try:
                print('starting queryset..................')
                m=Cbt_modules.objects.get(code=module)
                ques=Cbt_questions.objects.filter(module=m).order_by('?')
                qset=  ques
                
                print('setting qset....................... ')
            except Exception as e:
                print(e)

        else:
            ques=qset
            print('setting ques....................... ')
        
        if ques.count()>0:
            request.session['sessionstart']=1
            print('sessionstart just set ............')
            if not request.session.has_key('module'):
                request.session['module']=module
                request.session['duration']=time_lenght
                request.session.set_expiry(0)
                print('expire is......... ',request.session.get_expiry_age())
                print('session set....................... to ',request.session['module'])
            
            tim
            paginator=Paginator(ques,1)
            if not request.session.has_key('pagenum'):
                request.session['pagenum']=0
            
            if step == -1:
                pagenum=request.session['pagenum']-1
            else:        
                pagenum=request.session['pagenum']+1
            print('pagenum........',pagenum)
            request.session['pagenum']=pagenum
            if pagenum>paginator.count:
                pagenum=1
                request.session['pagenum']=1
            if pagenum<1:
                pagenum=1
                request.session['pagenum']=1

            question=paginator.page(pagenum)
            return render(
                request,
                'app/questionpage.html',
                {
                    'title':'About',
                    'message':'Your application description page.',
                    'year':datetime.now().year,
                    'questions':question,
                    'pagenum':pagenum,
                    'duration':time_lenght
                }
            )
    return HttpResponseRedirect('/boardpage/')
def legible(request):
    pass
def get_answer(request):
    mn=request.session.get('matricno',0)
    answeredlist=''
    qlist=''
    if mn != 0:
        mod=request.session.get('module','')
        if mod != '':
            answered=Cbt_ExamSession.objects.filter(student=Cbt_students.objects.get(matricnumber=mn),question__module__code=mod)
            answeredlist=[ans.question.question for ans in answered]
            ques=Cbt_questions.objects.filter(module__code=mod)
            qlist=[q.question for q in ques]
    return JsonResponse({'ans':answeredlist,'ques':qlist})

def questionpage(request):
    print('inside view.......................')
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    module= request.GET.get('module')
    print(module," selected....................")
    
    if request.session.get('sessionstarted',0) !=1:
        print('Creating sessions.............................................................')
        request.session['sessionstarted']=1
        request.session['candidate']=request.user.username
        request.session['module']=module

    m=Cbt_modules.objects.get(code=module)
    ques=Cbt_questions.objects.filter(module=m)
    scheduledexam=CBT_Exam.objects.get(module=m)
    time_lenght=scheduledexam.time_length
    print('Time length.........................',time_lenght)
    if request.session.get('questioncode',0) ==0:
        request.session['questioncode']=ques[0].question_code

    if ques.count() < 1:
        return HttpResponseRedirect('/boardpage/')

    page=request.GET.get('page',1)
    paginator=Paginator(ques,1)

    prev_ans=""
    answered=""
    answeredlist=[]
    qlist=[]

    try:
        questions=paginator.page(page)
        #saving the pk of the question to the session object
        #we are using this shutcut bcos we know that there is only one question per page
        request.session['qkey']=questions.object_list[0].pk

    except PageNotAnInteger:
        questions=paginator.page(1)
    except EmptyPage:
        questions=paginator.page(paginator.num_pages)
    
    l1=""
    has_ans=False
    try:
        
        answered=Cbt_ExamSession.objects.filter(student=Cbt_students.objects.get(matricnumber=request.session['matricno']),question__module__code=module)
        answeredlist=[ans.question.question for ans in answered]
        qlist=[q.question for q in ques]
        sessionque=Cbt_ExamSession.objects.get(question=Cbt_questions.objects.get(pk=questions.object_list[0].pk),student=Cbt_students.objects.get(matricnumber=request.session['matricno']))
        prev_ans=sessionque.studentchoice
        print('prevchoice.............................................',prev_ans)
        has_ans=True                         

        transchoice={'a':'0','b':'1','c':'2','d':'3','e':'4','f':'5','g':'6','h':'7','i':'8'}
        #print('transchoice[2]...................',transchoice[2])
        prevchoice=prev_ans.split('-')
        
        for choice in prevchoice:
            print('choice.........................',choice)
            if choice !='':
                l1=l1+transchoice[choice]+'-'
    
        print('reconstructed choice....................................',l1.strip('-'))



    except Exception as e:
        print('EROR...........................................',e)
    print('qqqqqqqqqqqqqqqqqqqqq....',questions.paginator.page_range)
    return render(request,'app/questionpage.html',
                  {
                   'questions':questions,
                   'module':module,
                   'duration':time_lenght,
                   'prev_ans':l1.strip('-'),
                   'has_ans':has_ans,
                   'answeredlist':answeredlist,
                   'qlist':qlist
                   })







    



