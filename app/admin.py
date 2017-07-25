from django.contrib import admin
from app.models import *
from django import forms
from django.shortcuts import render,redirect
admin.site.site_header="FCES"
admin.site.site_title="FCES-CBT Administration"
admin.site.register(Cbt_role)
from django.http import HttpResponseRedirect
from django.contrib.admin.models import LogEntry
from import_export.admin import ImportExportModelAdmin
from import_export import resources
admin.site.register(LogEntry)

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
    
    list_display=('username','email','matricnumber')
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
        'fields': (('question','question_with_image','question_image'), 'level', 'semester','module','creator','questiontype')
    }),
    ('Answer and Options', {
        'classes': ('collapse',),
        'fields': (('optionA','optionA_with_image','optionA_image'), 
                   ('optionB','optionB_with_image','optionB_image'), 
                   ('optionC','optionC_with_image','optionC_image'), 
                   ('optionD','optionD_with_image','optionD_image'),
                   ( 'answer'))
    }),
    ('Additional Options', {
        'classes': ('collapse',),
        'fields': (('optionE','optionE_with_image','optionE_image'), 
                   ('optionF','optionF_with_image','optionF_image'), 
                   ('optionG','optionG_with_image','optionG_image'), 
                   ('optionH','optionH_with_image','optionH_image'),
                   ('optionI','optionI_with_image','optionI_image'),
                   ('optionJ','optionJ_with_image','optionJ_image'))
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
    list_display=('student','modulecode','examiner_answer','result','studentchoice','question_code','question')
    search_fields = ['student','question__module__code']
    list_filter=('question__module__code','student')
    
    def modulecode(self,obj):
        return obj.question.module
    def examiner_answer(self,obj):
        return obj.question.answer
    def question_code(self,obj):
        return obj.question.question_code
    

admin.site.register(Cbt_ExamSession,Cbt_ExamSessionAdmin)

class StudentSessionResource(resources.ModelResource):
    class Meta:
        model=Cbt_StudentSession
        fields=('student','module','date','total_score','total_questions')
    def dehydrate_student(self,cbt_studentsession):
        return cbt_studentsession.student.username
    def dehydrate_module(self,cbt_studentsession):
        return cbt_studentsession.module.code       

class Cbt_StudentSessionAdmin(ImportExportModelAdmin):
    resource_class=StudentSessionResource
    list_display=('student','module','exam_status','date','total_attempt','total_score','total_questions')
    list_filter=('module','student')
    actions=['display_question','display_results']

    def display_question(self,request,queryset):
        student=queryset[0].student
        module=queryset[0].module
       
        return HttpResponseRedirect('/booklet/?student='+str(student)+'&module='+str(module))

    display_question.short_description="Display Booklet"     

    def display_results(self,request,queryset):
        print('*************'+str(queryset))
        return  render(request,'app/adminresults.html',{'results':queryset})

    display_results.short_description="Display Results"


admin.site.register(Cbt_StudentSession,Cbt_StudentSessionAdmin)

