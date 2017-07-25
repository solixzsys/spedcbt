import os,django,sys
from django import template

p=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(0,p)
# print(sys.path)
# print('xxxxxx')
import app
from app.models import *
os.environ['DJANGO_SETTINGS_MODULE']='cbtv02.settings'
django.setup()


register=template.Library()

# {% if instance_release  exam.module  %} 

@register.tag(name='instance_release')
def is_instance_release(parser,token):
    try:
        # split_contents() knows not to split quoted strings.
        # tag_name, module = token.split_contents()
        bits=token.contents.split()
        print('args------------'+str(bits))
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return InstantRelease(bits[1],bits[3])    
    # exam=CBT_Exam.objects.filter(module=module)[0]   

class InstantRelease(template.Node):
    def __init__(self,module,varname):
        self.module=  template.Variable(module)
        self.varname=varname
    def render(self,context):
        release =CBT_Exam.objects.filter(module=self.module.resolve(context))[0].instant_release
        context[self.varname]=release
        return ''
    
         