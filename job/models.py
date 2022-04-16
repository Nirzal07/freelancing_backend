from django.db import models
# from .choices import ListingType, ApplyThrough, EducationChoices, ExperienceChoices
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed
from .managers import JobModelManager, CategoryManager
from .choices import ExperienceChoices, ListingType
import datetime

class AbstractModel(models.Model):
    title = models.CharField(unique= True, max_length=50)

    class Meta:
        abstract = True
    def __str__(self):
        return self.title


    def save(self, *args, **kwargs): # new
        self.title = self.title.title()
        return super().save(*args, **kwargs)

def category_image_upload(instance, filename):
    return '/'.join(['CategoryImages', instance.title, filename ])
class Category(AbstractModel):
    objects = CategoryManager()
    
    image = models.ImageField(upload_to= category_image_upload, null= True, blank= True)
    no_of_openings = models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Categories'

class Address(AbstractModel):
    pass

class Skills(AbstractModel):
    pass

class Job(models.Model):
    objects= JobModelManager()
    
    # Prod Note: change set_null into restrict
    client                = models.ForeignKey("users.ClientAccount", on_delete=models.SET_NULL, null=True, default=1)
    title                   = models.CharField(max_length=100)
    category                = models.ForeignKey(Category, related_name='category', on_delete=models.SET_NULL, null=True,  default=1)
    # listing_type            = models.CharField(max_length=20, choices=ListingType, default=ListingType[0][0])
    price_is_range          = models.BooleanField(default=True)
    price                  = models.PositiveIntegerField(blank=True)
    min_price                  = models.PositiveIntegerField()
    max_price                  = models.PositiveIntegerField()
    # no_of_vacancies         = models.IntegerField(default=1)
    description             = models.TextField(blank= True)
    # experience              = models.CharField(max_length= 20, choices=ExperienceChoices)
    skills                  = models.ManyToManyField('job.Skills')
    # deadline                = models.DateField()
    views                   = models.PositiveIntegerField(default= 0)
    slug                    = models.SlugField(unique=True)

    announced_date            = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return self.title
    @property
    def category_image(self):
        if self.category.image:
            return self.category.image.url
        return
    @property
    def is_available(self):
        # if deadline is exceeded return false else return true
        pass

    @property
    def announced_on(self):
        now = datetime.datetime.now().astimezone()
        s = str(now-self.announced_date).split(",")
        return f'{s[0]} ago' if len(s) >= 2 else "Today"

    def save(self, *args, **kwargs):
        if self.price_is_range:
            self.price = (self.min_price + self.max_price) / 2
        return super().save(*args, **kwargs)

    # @property
    # def price_amount(self):
    #     if not self.price_is_range:
    #         return int(self.price)
    #     return 0
    
    # @property
    # def min_price(self):
    #     if self.price_is_range and self.price.contains('-'):
    #         return int(self.price.split('-')[0])
    #     return int(self.price)
    
    # @property
    # def max_price(self):
    #     if self.price_is_range and self.price.contains('-'):
    #         return int(self.price.split('-')[1])
    #     return int(self.price)
    

@receiver(post_save, sender=Job)
def update_job_slug(sender, instance, created = False, **kwargs):
    if not instance.slug:
        instance.slug = slugify( f"{instance.id}-{instance.title}" )
        instance.title = instance.title.title()
        instance.save()

@receiver(post_save, sender=Job)
def update_categories_noofopening(sender, instance, created = False, **kwargs):
    category = instance.category
    category.no_of_openings = len(Job.objects.filter(category=category))
    category.save()

# class Favourites(models.Model):
#     """
    
#     """
#     user = models.OneToOneField("accounts.User", on_delete=models.RESTRICT)
#     favourite_jobs = models.ManyToManyField("job.Job")
#     added_on = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = 'Favourites'
#         verbose_name_plural = 'Favourites'

#     def __str__(self):
#         return f"{self.user.email_or_phone}'s Favourites"
    
class Proposals(models.Model):
    job = models.OneToOneField("job.Job", on_delete=models.CASCADE)
    proposants = models.ManyToManyField("users.FreelancerAccount")

    class Meta:
        verbose_name = 'Proposals'
        verbose_name_plural = 'Proposals'

    def __str__(self):
        return f"{self.job.title}'s Proposals"

class ProposedJobs(models.Model):

    freelancer = models.OneToOneField("users.FreelancerAccount", on_delete=models.RESTRICT)
    jobs = models.ManyToManyField("job.Job")

    class Meta:
        verbose_name = 'Applied Job'
        verbose_name_plural = 'Applied Jobs'

    def __str__(self):
        return f"{self.freelancer.full_name}'s ProposedJobs"

@receiver(m2m_changed, sender=ProposedJobs.jobs.through)
def proposed_jobs_changed(sender, pk_set, action, instance, **kwargs):
    for id in pk_set:
        job= Job.objects.get(id=id)
        client = job.client
        try:
            proposants = Proposals.objects.get(job= job)
        except Proposals.DoesNotExist:
            proposants = Proposals.objects.create(job=job)
        if action == "post_add" :
            proposants.proposants.add(instance.freelancer)
        if action == "post_remove" :
            proposants.proposants.remove(instance.freelancer)
        if action == "post_clear" :
            proposants.proposants.remove(instance.freelancer)