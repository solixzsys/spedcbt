from django.contrib import admin
from app.models import *

admin.site.site_header="fxSoftLogix CBT"
admin.site.site_title="CBT Administration"
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
class Cbt_studentAdmin(admin.ModelAdmin):
    list_display=('username','email','matricnumber')
    search_fields = ['username','matricnumber']
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

class CBT_ExamAdmin(admin.ModelAdmin):
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
    list_filter=('question__module__code',)
    def modulecode(self,obj):
        return obj.question.module
    def examiner_answer(self,obj):
        return obj.question.answer

admin.site.register(Cbt_ExamSession,Cbt_ExamSessionAdmin)

class Cbt_StudentSessionAdmin(admin.ModelAdmin):
    list_display=('student','module','exam_status','date','total_attempt','total_score')





admin.site.register(Cbt_StudentSession,Cbt_StudentSessionAdmin)