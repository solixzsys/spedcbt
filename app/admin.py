from django.contrib import admin
from app.models import *
from django import forms

admin.site.site_header="fxSoftLogix"
admin.site.site_title="CBTCUBE Administration"
admin.site.register(Cbt_role)
from django.http import HttpResponseRedirect


class Cbt_examinerAdmin(admin.ModelAdmin):
    def examiner_name(self,obj):
        return obj.user.username
    list_display=('staffid','examiner_name',)
    filter_horizontal=('modules',)


admin.site.register(Cbt_examiner,Cbt_examinerAdmin)
admin.site.register(Cbt_user)

class Cbt_modulesAdmin(admin.ModelAdmin):
    list_display=('code','name','status')
    

admin.site.register(Cbt_modules,Cbt_modulesAdmin)
admin.site.register(Cbt_semester)

class Cbt_studentAdminForm(forms.ModelForm):
    class Meta:
        model=Cbt_students
        exclude=('username',)
        widgets={
            'password':forms.PasswordInput(),
            }

class Cbt_studentAdmin(admin.ModelAdmin):
    form=Cbt_studentAdminForm
    
    list_display=('firstname','email','matricnumber')
    search_fields = ['firstname','matricnumber']



    def save_model(self, request, obj, form, change):
        print('^^^^^^^^^^^^^^^^^^^  ',obj.username)
        self.username=obj.firstname+"_"+obj.matricnumber
        try:
            u=User.objects.get(username=self.username)
            #u.username=self.username,
            u.set_password(obj.password)
            u.first_name=obj.firstname
            u.last_name=obj.lastname
            u.email=obj.email
            u.save()
        except:

            User.objects.create_user(username=self.username,
                                password=obj.password,
                                first_name=obj.firstname,
                                last_name=obj.lastname,
                                email=obj.email
                                )

        
        return super().save_model(request, obj, form, change)
admin.site.register(Cbt_students,Cbt_studentAdmin)
admin.site.register(Cbt_level)





class Cbt_facultyAdmin(admin.ModelAdmin):
    filter_horizontal=('department',)


    

admin.site.register(Cbt_faculty,Cbt_facultyAdmin)

class Cbt_departmentAdmin(admin.ModelAdmin):
    filter_horizontal=('moduless',)
admin.site.register(Cbt_department,Cbt_departmentAdmin)

admin.site.register(Cbt_sessions)





class Cbt_questionAdmin(admin.ModelAdmin):
    list_display=('question_code','question','scheduled','module','questiontype')
    list_filter=('module__code',)
    def get_queryset(self, request):
        qs= super(Cbt_questionAdmin,self).get_queryset(self)
        if request.user.is_superuser:
            return qs
        return qs.filter(creator=Cbt_examiner.objects.get(user=request.user))
   

    fieldsets = (
    (None, {
        'fields': ('question', 'level', 'semester','module','creator','questiontype')
    }),
    ('Answer and Options', {
        'classes': ('collapse',),
        'fields': ('optionA', 'optionB', 'optionC', 'optionD', 'answer')
    }),
    ('Additional Options', {
        'classes': ('collapse',),
        'fields': ('optionE', 'optionF', 'optionG', 'optionH', 'optionI', 'optionJ')
    }),
)
admin.site.register(Cbt_questions,Cbt_questionAdmin)


from django.contrib.auth.models import User

class CBT_ExamAdminForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(CBT_ExamAdminForm,self).__init__(*args,**kwargs)
        self.fields['exam_owner'].queryset=User.objects.filter(is_staff=True)


class CBT_ExamAdmin(admin.ModelAdmin):
    form=CBT_ExamAdminForm
    list_display=('module','exam_date','status','exam_owner','level','time_length','instant_release')
    filter_horizontal=('exclussion',)

    def save_model(self, request, obj, form, change):
        user=request.user
        print("{} schedule an {} exam".format(user,obj))
        
        mod=Cbt_modules.objects.get(code=obj.module)      


        mod.status=obj.status
        mod.save()
        ques=Cbt_questions.objects.filter(module=mod).update(scheduled=True)
        print('mod ',obj.module)
        print('ques ',ques)
        return super().save_model(request, obj, form, change)

admin.site.register(CBT_Exam,CBT_ExamAdmin)

class Cbt_ExamSessionAdmin(admin.ModelAdmin):
    list_display=('student','modulecode','question','studentchoice','examiner_answer','result')
    search_fields = ['student','question__module__code']
    list_filter=('question__module__code','student')
    def modulecode(self,obj):
        return obj.question.module
    def examiner_answer(self,obj):
        return obj.question.answer

admin.site.register(Cbt_ExamSession,Cbt_ExamSessionAdmin)

class Cbt_StudentSessionAdmin(admin.ModelAdmin):
    list_display=('student','module','exam_status','date','total_attempt','total_score','total_questions')
    list_filter=('module','student')




admin.site.register(Cbt_StudentSession,Cbt_StudentSessionAdmin)