from django.contrib import admin
from .models import Address, Category, Skills
from .models import Job, ProposedJobs, Proposals

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

@admin.register(Proposals)
class ProposalsAdmin(admin.ModelAdmin):
    pass
