from django import template
# Create your models here.


register=template.Library()

@register.filter
def get_at_index(list,index):
    
    return list[index]