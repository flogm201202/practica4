from django.contrib import admin
from .models import Library, Book, Loan, User
admin.site.register(Library)
admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(User)
