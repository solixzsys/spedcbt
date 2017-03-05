"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import  User
from datetime import datetime
from django.core.exceptions import ValidationError






class Cbt_role(models.Model):
    role_name=models.CharField(max_length=200)
    class Meta:
        verbose_name='CBT ROLE'
        verbose_name_plural='CBT ROLES'

    def __str__(self):
        return str(self.role_name)

class Cbt_user(models.Model):
    firstname=models.CharField(max_length=200,blank=True)
    surname=models.CharField(max_length=200,blank=True)
    middlename=models.CharField(max_length=200,blank=True)
    username=models.CharField(max_length=200,blank=True)
    

    def save(self,**kwargs):
        self.username=self.firstname+"_"+self.middlename
        return super().save(**kwargs)

    def __str__(self):
        return str(self.username)

class Cbt_modules(models.Model):

    MODULE_STATUS_CHOICES=(
        ('UNSCHEDULED','UNSCHEDULED'),
        ('SCHEDULED','SCHEDULED'),
        ('IN-PROGRESS','IN-PROGRESS'),
        ('ENDED','ENDED')
        )

    name=models.CharField(max_length=200)
    code=models.CharField(max_length=10)
    status=models.CharField(max_length=20,choices=MODULE_STATUS_CHOICES,default='UNSCHEDULED')
    class Meta:
        verbose_name='CBT MODULE'
        verbose_name_plural='CBT MODULES'
        
    def __str__(self):

        return "{}".format(self.code)

class Cbt_department(models.Model):
    name=models.CharField(max_length=200)
    moduless=models.ManyToManyField(Cbt_modules,blank=True)

    class Meta:
        verbose_name='CBT DEPARTMENT'
        verbose_name_plural='CBT DEPARTMENTS'
    def __str__(self):

        return "{}".format(self.name)



class Cbt_examiner(models.Model):
    user=models.OneToOneField(User)
    staffid=models.CharField(max_length=10)
    modules=models.ManyToManyField(Cbt_modules,blank=True)

    class Meta:
        verbose_name='CBT EXAMINER'
        verbose_name_plural='CBT EXAMINER'
    def __str__(self):
        return self.user.username


class Cbt_faculty(models.Model):
    name=models.CharField(max_length=200)
    department=models.ManyToManyField(Cbt_department,default="")

    class Meta:
        verbose_name='CBT FACULTY'
        verbose_name_plural='CBT FACULTIES'

    def __str__(self):

        return "{}".format(self.name).upper()

class Cbt_level(models.Model):
    name=models.CharField(max_length=10,default="100L")

    class Meta:
        verbose_name='CBT LEVEL'
        verbose_name_plural='CBT LEVELS'
    def save(self,**kwargs):
        self.name=self.name.upper()
        return super().save(**kwargs)

    def __str__(self):

        return self.name

class Cbt_semester(models.Model):
    SEMESTERS=(
        ("FIRST SEMESTER","FIRST SEMESTER"),
               
       ("SECOND SEMESTER","SECOND SEMESTER"),
       )
    name=models.CharField(max_length=20,choices=SEMESTERS,default="")

    class Meta:
        verbose_name='CBT SEMESTER'
        verbose_name_plural='CBT SEMESTERS'

    def __str__(self):
        return self.name
    


        
class Cbt_questions(models.Model):


    def photopath(self,filename):

        return 'question/'+self.module.code+'/'+str(datetime.today().year)+'/'+str(datetime.today().month)+'/'+filename

    QUESTION_TYPES=(
    ('SINGLE','SINGLE'),
    ('MULTIPLE','MULTIPLE')
    )

    question=models.TextField(default="")
    question_with_image=models.BooleanField(default=False)
    question_image=models.FileField(upload_to=photopath,blank=True)
    question_code=models.CharField(max_length=50,default="")
    level=models.ForeignKey(Cbt_level,default="")
    semester=models.ForeignKey(Cbt_semester,default="")
    module=models.ForeignKey(Cbt_modules,default="")
    scheduled=models.BooleanField(default=False)
    creator=models.ForeignKey(Cbt_examiner)
    questiontype=models.CharField(max_length=20,choices=QUESTION_TYPES,default='SINGLE',blank=True)
    answer=models.CharField(max_length=10,default="",blank=True)
    #answerd=models.BooleanField(default=False)
    optionA=models.CharField(max_length=200,default="",blank=True,verbose_name="Option A")
    optionA_with_image=models.BooleanField(default=False)
    optionA_image=models.FileField(upload_to='question/%Y/%m/%d',blank=True)
    optionB=models.CharField(max_length=200,default="",blank=True,verbose_name="Option B")
    optionB_with_image=models.BooleanField(default=False)
    optionB_image=models.FileField(upload_to='question/%Y/%m/%d',blank=True)
    optionC=models.CharField(max_length=200,default="",blank=True,verbose_name="Option C")
    optionC_with_image=models.BooleanField(default=False)
    optionC_image=models.FileField(upload_to='question/%Y/%m/%d',blank=True)
    optionD=models.CharField(max_length=200,default="",blank=True,verbose_name="Option D")
    optionD_with_image=models.BooleanField(default=False)
    optionD_image=models.FileField(upload_to='question/%Y/%m/%d',blank=True)
    optionE=models.CharField(max_length=200,default="",blank=True,verbose_name="Option E")
    optionE_with_image=models.BooleanField(default=False)
    optionE_image=models.FileField(upload_to='question/%Y/%m/%d',blank=True)
    optionF=models.CharField(max_length=200,default="",blank=True,verbose_name="Option F")
    optionF_with_image=models.BooleanField(default=False)
    optionF_image=models.FileField(upload_to='question/%Y/%m/%d',blank=True)
    optionG=models.CharField(max_length=200,default="",blank=True,verbose_name="Option G")
    optionG_with_image=models.BooleanField(default=False)
    optionG_image=models.FileField(upload_to='question/%Y/%m/%d',blank=True)
    optionH=models.CharField(max_length=200,default="",blank=True,verbose_name="Option H")
    optionH_with_image=models.BooleanField(default=False)
    optionH_image=models.FileField(upload_to='question/%Y/%m/%d',blank=True)
    optionI=models.CharField(max_length=200,default="",blank=True,verbose_name="Option I")
    optionI_with_image=models.BooleanField(default=False)
    optionI_image=models.FileField(upload_to='question/%Y/%m/%d',blank=True)
    optionJ=models.CharField(max_length=200,default="",blank=True,verbose_name="Option J")
    optionJ_with_image=models.BooleanField(default=False)
    optionJ_image=models.FileField(upload_to='question/%Y/%m/%d',blank=True)
    
    
    class Meta:
        verbose_name='CBT QUESTION'
        verbose_name_plural='CBT QUESTIONS'

    def metafield(self):
        return self._meta.get_fields()

    def save(self, **kwargs):
        self.question_code="{}-{}-{}-{}".format(self.module,self.level,self.semester,self.pk)
        
        return super().save(**kwargs)

    def __str__(self):

        return self.question

class Cbt_sessions(models.Model):
    name=models.CharField(max_length=10,default="")

    class Meta:
        verbose_name='CBT SESSION'
        verbose_name_plural='CBT SESSIONS'
    def __str__(self):

        return self.name
class Cbt_students(models.Model):
   

    firstname=models.CharField(max_length=200,blank=True)
    
    lastname=models.CharField(max_length=200,blank=True)
    middlename=models.CharField(max_length=200,blank=True)
    username=models.CharField(max_length=200,blank=True)
    password=models.CharField(max_length=200)
    matricnumber=models.CharField(max_length=20,unique=True)
    email=models.EmailField(blank=True,unique=True)
    phonenumber=models.CharField(max_length=20,blank=True)
    level=models.ForeignKey(Cbt_level)
    session=models.ForeignKey(Cbt_sessions)
    semester=models.ForeignKey(Cbt_semester)
    faculty=models.ForeignKey(Cbt_faculty)
    department=models.ForeignKey(Cbt_department)
    picture=models.FileField(upload_to='passport/%Y/%m/%d',blank=True)
    
    class Meta:
        verbose_name='CBT STUDENT'
        verbose_name_plural='CBT STUDENTS'

    def __str__(self):

        return "{}".format(self.username)

    def save(self,**kwargs):
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^ saving student')
        self.username=self.firstname+"_"+self.matricnumber
        return super().save(**kwargs)
#class Cbt_students(models.Model):
   

#    firstname=models.CharField(max_length=200,blank=True)
    
#    lastname=models.CharField(max_length=200,blank=True)
#    middlename=models.CharField(max_length=200,blank=True)
#    username=models.CharField(max_length=200,blank=True)
#    password=models.CharField(max_length=200,blank=True)
#    matricnumber=models.CharField(max_length=20,unique=True)
#    email=models.EmailField(blank=True,unique=True)
#    phonenumber=models.CharField(max_length=20,blank=True)
#    level=models.ForeignKey(Cbt_level)
#    session=models.ForeignKey(Cbt_sessions)
#    semester=models.ForeignKey(Cbt_semester)
#    faculty=models.ForeignKey(Cbt_faculty)
#    department=models.ForeignKey(Cbt_department)
#    picture=models.FileField(upload_to='passport/%Y/%m/%d',blank=True)
    
#    class Meta:
#        verbose_name='CBT STUDENT'
#        verbose_name_plural='CBT STUDENTS'

#    def __str__(self):

#        return "{}".format(self.username)

#    def save(self,**kwargs):
#        print('^^^^^^^^^^^^^^^^^^^^^^^^^^ saving student')
#        self.username=self.firstname+"_"+self.matricnumber
#        return super().save(**kwargs)

class CBT_Exam(models.Model):
    #status choices
    STATUS_CHOICES=(
        ('SCHEDULED','SCHEDULED'),
        ('IN PROGRESS','IN PROGRESS'),
        ('ENDED','ENDED')
        )
    #exam date
    exam_date=models.DateTimeField()
    #module
    module=models.ForeignKey(Cbt_modules,unique=True)
    #duration
    time_length=models.IntegerField()
    #exam owner
    exam_owner=models.ForeignKey(User)
    #schedule stage
    status=models.CharField(max_length=200,choices=STATUS_CHOICES,default='SCHEDULED')
    instant_release=models.BooleanField(default=True)
    level=models.ForeignKey(Cbt_level,blank=True,null=True)
    exclussion=models.ManyToManyField(Cbt_students,blank=True,null=True)
    class Meta:
        verbose_name='CBT EXAM'
        verbose_name_plural='CBT EXAMS'

    def __str__(self):
        return "{} ".format(self.module)

    def clean(self):
        if len(Cbt_questions.objects.filter(module=self.module))<1:
            raise ValidationError('Please, the Questions for the '+ self.module.code + ' has not been Uploaded Yet !!!')
        super(CBT_Exam,self).clean()


    def save(self, *args, **kwargs):
        #self.exam_owner= User.objects.filter(is_staff=True)
        self.full_clean()
        super().save(*args,**kwargs)

class Cbt_ExamSession(models.Model):
    student=models.ForeignKey(Cbt_students,blank=True,null=True)
    question=models.ForeignKey(Cbt_questions)
    studentchoice=models.CharField(max_length=20)
    result=models.IntegerField()

    class Meta:
        verbose_name='CBT EXAMSESSION'
        verbose_name_plural='CBT EXAMSESSIONS'


class Cbt_StudentSession(models.Model):
    EXAMS_STATUS=(('NONE','NONE'),('STARTED','STARTED'),('FINISHED','FINISHED'),)
    student=models.ForeignKey(Cbt_students)
    module=models.ForeignKey(Cbt_modules)
    exam_status=models.CharField(max_length=20,choices=EXAMS_STATUS,default='NONE')
    date=models.DateTimeField(blank=True)
    total_score=models.IntegerField(default=0)
    total_attempt=models.IntegerField(default=0)
    total_questions=models.IntegerField(default=0)

    def save(self,**kwargs):
        
        self.total_questions= Cbt_questions.objects.filter(module=self.module).count()
        return super().save(**kwargs)
