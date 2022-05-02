from django.contrib import admin
from .models import Address, Category, Skills
from .models import Job, ProposedJobs, Proposal, JobRequest

class AbstractModelAdmin(admin.ModelAdmin):
    # add account.companyname whereever necessary
    list_display = ['id', 'title']
    list_display_links = ['title']
    ordering = ('title',)
    search_fields = ('title',)


class AbstractJobAdmin(admin.ModelAdmin):
    # add account.companyname whereever necessary
    list_display = ['id', 'title',]
    list_display_links = ['id', 'title']
    ordering = ()
    search_fields = ('title',)
    readonly_fields =()

@admin.register(Job)
class JobAdmin(AbstractJobAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(AbstractModelAdmin):
    pass

@admin.register(Address)
class AddressAdmin(AbstractModelAdmin):
    pass

@admin.register(Skills)
class SkillsAdmin(AbstractModelAdmin):
    pass

# @admin.register(Favourites)
# class FavouritesAdmin(admin.ModelAdmin):
#     pass

@admin.register(ProposedJobs)
class ProposedJobsAdmin(admin.ModelAdmin):
    pass

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['id', 'job', 'proposant',]
    list_display_links = ['id', 'job', 'proposant']
    search_fields = ('job', 'proposant', )
    ordering = ('job', 'proposant',)

@admin.register(JobRequest)
class JobRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'job', 'freelancer',]
    list_display_links = ['id', 'job', 'freelancer']
    search_fields = ('job', 'freelancer', )
    ordering = ('job', 'freelancer',)