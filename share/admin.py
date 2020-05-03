# Module 1
# Register new models
from django.contrib import admin

from .models import Script, Problem, Coder, Review   #.models because models.py it is in the same folder

admin.site.register(Script)
admin.site.register(Problem)
admin.site.register(Coder)
admin.site.register(Review)
