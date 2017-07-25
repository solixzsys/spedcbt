import os,django,sys
from django import template
# from django.db.models import Q
# p=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# sys.path.insert(0,p)
# # print(sys.path)
# # print('xxxxxx')
# import app
# from app.models import *
# os.environ['DJANGO_SETTINGS_MODULE']='cbtv02.settings'
# django.setup()


register=template.Library()

# {% if instance_release  exam.module  %} 

@register.tag(name='colorize')
def begin_check(parser,token):
    try:
        # split_contents() knows not to split quoted strings.
        # tag_name, module = token.split_contents()
        bits=token.contents.split()
        print('args------------'+str(bits))
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return check_result(bits[1],bits[2])    
    # exam=CBT_Exam.objects.filter(module=module)[0]   

class check_result(template.Node):
    def __init__(self,choice,answer):
        self.choice=  template.Variable(choice)
        self.answer=template.Variable(answer)
        
       
    def render(self,context):
        
        # student_obj=Cbt_students.objects.get(username=self.student.resolve(context))
        # question_obj=Cbt_questions.objects.get(question_code=self.code.resolve(context))
        # # print('&&&&&&&&&&&&&&&&&&'+str(question_obj))
        # try:
        #     option=Cbt_ExamSession.objects.get(Q(student=student_obj)& Q(question=question_obj))
        # except:
        color="" 
        # print('resolved args.............................'+str(self.choice.resolve(context))+'  '+str(self.answer.resolve(context)))
        try:   
            if self.choice.resolve(context) != self.answer.resolve(context):
                color='red'
        except:
            color='#009999'      
            
        context['color']=color
        return ''
    
         