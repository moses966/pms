**How to customize django admin groups by subclassing the built-in Group model.**
We are going to customize the django admin such that, we can rename the Groups model and replace it  
with our own custom model.  
1. First, create a file and name it `customs.py`
2. populate it with the following code so as to create a model for departments which subclasses Group model:
3. ```python
   from django.contrib.auth.models import Group
   from django.db import models

   # model for departments
   class Departments(Group):
       class Meta:
           verbose_name = "Department"
           verbose_name_plural = "Departments"
   ```
4. In your models.py file, create a model that customizes the Department(groups) the way you want:
5. ```python
   # model to customize the group model
   class CustomGroup(models.Model):
       group = models.OneToOneField(Departments, on_delete=models.CASCADE, primary_key=True)
       leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='department_leader')

       def __str__(self):
           return self.group.name
   ```
6. In the admin.py file, add the following activities:
7. ```python
   # customized group
   class CustomGroupInline(admin.StackedInline):
       model = CustomGroup
       can_delete = False
       verbose_name = 'Department Head'
       verbose_name_plural = 'Department Heads'
    
   # add the CustomGroup wiget to the admin interface
   class CustomGroupAdmin(GroupAdmin):
       inlines = (CustomGroupInline,)

   #unregister default and register custom group
   admin.site.unregister(Group)
   admin.site.register(Departments, CustomGroupAdmin)
   ```
8. You can then run migrations.
