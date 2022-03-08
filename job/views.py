from rest_framework import status
from rest_framework.response import Response
# from .populate import populate_db
from django.db.utils import OperationalError, ProgrammingError
from users.models import ClientAccount, FreelancerAccount, User
from django_filters import rest_framework as filters
from django_filters import MultipleChoiceFilter

from .serializers import ( ProposalsSerializer, 
                          AddressSerializer,
                          CategorySerializer,
                          SkillsSerializer,
                          JobSerializer,
                          FavouritesSerializer,
                          ProposedJobsSerializer
                          )

from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    ListAPIView
    )
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import (
    Job,
    Address,
    Category,
    # Favourites,
    Skills,
    Proposals,
    ProposedJobs
    )

import users.models as user_models 
import users.serializers as user_serializers 

from django.db.models import Q
from django.utils import  timezone
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.core.signals import request_finished



def get_popular_categories():
    popular_categories= []
    for popular_category in Category.objects.all().order_by():
        popular_categories.append({"category_id": popular_category.id, "category_title": popular_category.title, "number_of_openings": popular_category.no_of_openings})
    return popular_categories

def get_jobs_from_random_categories(no_of_items):
    """"""
    ids = Category.objects.all().values_list('id')
    id_list = [value[0] for value in ids]
    
    random_cat_jobs = []
    for id in id_list:
        category = Category.objects.get(id = id)
        category_jobs = Job.jobs.filter(category=category)[:no_of_items]
        category_jobs_serializer= JobSerializer(category_jobs, many=True)
        job = {'category_title':category.title , 'jobs' : category_jobs_serializer.data}
        random_cat_jobs.append(job)
    return random_cat_jobs
        
class HomePage(APIView):
    def get(self, request, format=None):
        # featured and popular jobs
        job_display_no= 4
        standard_jobs = Job.objects.standard()[:job_display_no]
        standard_serializer = JobSerializer(standard_jobs, many=True)
        
        featured_freelancers = FreelancerAccount.objects.standard()[:job_display_no]
        featured_freelancers_serializer = user_serializers.FreelancerAccountSerializer(featured_freelancers, many=True)
        
        featured_jobs = Job.objects.standard()[:job_display_no]
        featured_serializer = JobSerializer(featured_jobs, many=True)
        
        premium_jobs = Job.objects.premium()[:job_display_no]
        premium_serializer = JobSerializer(premium_jobs, many=True)
        
        popular_jobs = Job.objects.popular()[:job_display_no]
        popular_serializer = JobSerializer(popular_jobs, many=True)
        
        popular_categories = Category.objects.popular()
        popular_category_serializer = CategorySerializer(popular_categories, many= True)


        datas = {
            'featured_jobs': featured_serializer.data,
            'featured_freelancers': featured_freelancers_serializer.data,
            'popular_categories': popular_category_serializer.data,
            # 'standard_jobs': standard_serializer.data,
            # 'premium_jobs': premium_serializer.data,
            # 'popular_jobs': popular_serializer.data,
            # 'random_categories' : get_jobs_from_random_categories(no_of_items=job_toshow)
            }
        return Response(datas, status=status.HTTP_200_OK)

class JobFilter(filters.FilterSet):
    try:
        cat_choices = [(cat, cat) for cat in Category.objects.all().values_list('title', flat=True)]
        address_choices = [(dis, dis) for dis in Address.objects.all().values_list('title', flat=True)]
    except (OperationalError, ProgrammingError) as e:
        cat_choices=[]
        address_choices=[]
        
    category = MultipleChoiceFilter(
        field_name='category__title',
        lookup_expr='exact',
        conjoined=True,  # uses AND instead of OR
        choices = cat_choices
    )
    
    address = MultipleChoiceFilter(
        field_name='client__address__title',
        lookup_expr='exact',
        conjoined=True,  # uses AND instead of OR
        choices = address_choices
    )
    
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    # education = filters.CharFilter(field_name="education", lookup_expr='icontains')
    # experience = filters.CharFilter(field_name="experience", lookup_expr='icontains')

    class Meta:
        model = Job
        fields = ['category', 'min_price', 'max_price', 'address']

class JobView(ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'description']
    filterset_class = JobFilter
    ordering_fields = ['announced_date', 'min_price', 'max_price', 'views']
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'slug'
    # permission_classes = (IsCreater,)

    
    # def retrieve(self, request, pk):
    #     queryset = Job.jobs.all()
    #     object = get_object_or_404(queryset, pk=pk)
    #     object.views += 1
    #     object.save()
    #     serializer = JobSerializer(object)
    #     data= serializer.data
    #     data['similar_jobs'] = get_similar_jobs(object)
    #     return Response(data)
    
class JobsListView(ListAPIView):
    """ 
    abstract class for featured, popular, recent jobs list
    """
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'description']
    filterset_class = JobFilter
    ordering_fields = ['title', 'salary']
    serializer_class = JobSerializer
    model = Job
    
    
class ProposedJobsView(APIView):
    """
    To get the list of a JobSeeker's applied job get is used
    
    To add item to the list post req with id of the job
    upon adding item an instance of proposants is created for the Employer
    
    To delet item delete req with id of the job
    upon deleting the item the applicant is removed from the list of proposants for the job
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """To get the list of a users Favourites job"""
        if self.request.user.is_freelancer:
            try:
                applicant = FreelancerAccount.objects.get(basic_user=self.request.user)
                proposed_jobs = ProposedJobs.objects.get(freelancer = applicant)
                serializer = ProposedJobsSerializer(proposed_jobs)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ProposedJobs.DoesNotExist:
                return Response({'message': "You haven't applied for any jobs yet"}, status=status.HTTP_200_OK)
        return Response({'message': "Employer Account cannot access this"}, status=status.HTTP_200_OK)
                
    def post(self, request):
        
        """To add item to the list post req with id of the job"""
        if self.request.user.is_freelancer:
            id = request.data['id']
            job = Job.objects.get(id= id)
            applicant = FreelancerAccount.objects.get(basic_user=self.request.user)
            try:
                applied_job= ProposedJobs.objects.get(
                    freelancer = applicant
                    )
            except ProposedJobs.DoesNotExist:
                applied_job= ProposedJobs.objects.create(
                    freelancer = applicant
                    ) 
                
            applied_job.jobs.add(job)
            applied_job.save()
            
            #simultaneously create Proposals instance with the JobSeeker as applicant
            try:
                proposants= Proposals.objects.get(
                    job = job
                    )
            except Proposals.DoesNotExist:
                proposants= Proposals(
                    job = job
                    ) 
            applicant = FreelancerAccount.objects.get(basic_user= self.request.user)
            proposants.proposants.add(applicant)
            proposants.save()
            
            return Response({'message': "Job Apply"}, status=status.HTTP_200_OK)
        return Response({'message': "Employer Account cannot access this"}, status=status.HTTP_200_OK)       
        
    def delete(self, request):
        id = request.data['id']
        job = Job.objects.get(id= id)
        applicant = FreelancerAccount.objects.get(basic_user=self.request.user)

        proposed_jobs= ProposedJobs.objects.get(
            freelancer = applicant)
        proposed_jobs.jobs.remove(job)
        proposed_jobs.save()
        
        proposants= Proposals.objects.get(
                job = job
                )
        proposants.proposants.remove(applicant)
        proposants.save()
        
        return Response({'message': "Job successfully removed from Applied Jobs"}, status=status.HTTP_200_OK)
                
                
class ProposalsView(APIView):
    """
    To get the list of a applied of a particular job

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """To get the list of a jobseeker's Proposals job"""
        if self.request.user.is_freelancer:
            try:
                client = ClientAccount.objects.get(basic_user=self.request.user)
                proposants = Proposals.objects.filter(job__client = client)
                serializer = ProposalsSerializer(proposants, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Proposals.DoesNotExist:
                return Response({'message': "No One has applied to your job"}, status=status.HTTP_200_OK)
        return Response({'message': "JobSeeker Account cannot access this"}, status=status.HTTP_200_OK)
                
 
class PostedJobsListView(APIView):
    """
    To get the list of a applied of a particular job

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """To get the list of a client's Posted job"""
        if self.request.user.is_freelancer:
            try:
                client = ClientAccount.objects.get(basic_user = self.request.user)
                posted_jobs = Job.jobs.filter(client = client)
                serializer = JobSerializer(posted_jobs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Job.DoesNotExist:
                return Response({'message': "You have not posted any jobs yet"}, status=status.HTTP_200_OK)
        return Response({'message': "JobSeeker Account cannot access this"}, status=status.HTTP_200_OK)
          
    
class FeaturedJobsListView(JobsListView):
    def get_queryset(self):
        queryset = self.model.jobs.featured()
        return queryset
    
class PopularJobsListView(JobsListView):
    def get_queryset(self):
        queryset = self.model.jobs.popular()
        return queryset
    
class RecentJobsListView(JobsListView):
    def get_queryset(self):
        queryset = self.model.jobs.recent()
        return queryset
                
class AddressView(APIView):
    def get(self, request, *args, **kwargs):
        addresss = Address.objects.all()
        serializer= AddressSerializer(addresss, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)

class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        job_categories = Category.objects.all()
        serializer= CategorySerializer(job_categories, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
class SkillsView(APIView):
    def get(self, request, *args, **kwargs):
        skills = Skills.objects.all()
        serializer= SkillsSerializer(skills, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    


# def get_similar_jobs(job):
#     similar_jobs = Job.jobs.filter(
#         Q(category=job.category) |
#         Q(area__icontains=job.area) |
#         Q(title__icontains=job.title)
#     )[:10]
#     serializer = JobSerializer(similar_jobs, many=True)
#     return serializer.data
# class RecommendedJobsListView(APIView):
    
#     def get(self, request, *args, **kwargs):
#         if not self.request.user.is_freelancer:
#             freelancer_user = FreelancerAccount.objects.get(basic_user = self.request.user)
            
#             # from favourites
#              # get two parameter from last fav_job ie title and category
#             if Favourites.objects.filter(user = self.request.user).exists():
#                 fav_job = Favourites.objects.get(user = self.request.user).favourite_jobs[-1]
#                 recommended_from_favourite_job_title = Q(title = fav_job.title)
#                 recommended_from_favourite_job_cat = Q(category__title = fav_job.category.title)
            
#             # from preferred categories
#              # if a job from recent job
#             if freelancer_user.preferred_job_category:
#                 preferred_job_cat = freelancer_user.preferred_job_category
#                 for recent_jobs in Job.jobs.recent():
#                     if recent_jobs.category.title in preferred_job_cat:
#                         recommended_from_recent_jobs = Q(category__title = recent_jobs.category.title)
#                         break
#                 # recommended_from_users_preffered_cat = Q(category__title = recent_jobs.category.title)

                    
#             if freelancer_user.area:
#                 recommended_from_job_address = Q(area__icontains = freelancer_user.area)
                   
#             recommended_jobs = Job.jobs.filter(
#                 recommended_from_favourite_job_title |
#                 recommended_from_favourite_job_cat |
#                 recommended_from_job_address |
#                 recommended_from_recent_jobs
#             )
#             serializer= JobSerializer(recommended_jobs, many= True)
#             return Response(serializer.data, status= status.HTTP_200_OK)


# class FavouritesView(APIView):
#     """
#     To get the list of a users Favourites job get is used
#     To add item to the list post req with id of the job
#     To delet item delete req with id of the job
#     """
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         """To get the list of a users Favourites job"""
#         try:
#             favourite_jobs = Favourites.objects.get(user = self.request.user)
#             serializer = FavouritesSerializer(favourite_jobs)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Favourites.DoesNotExist:
#             return Response({'message': "You do not have any Favourites jobs"}, status=status.HTTP_200_OK)
            
#     def post(self, request):
#         """To add item to the list post req with id of the job"""
#         id = request.data['id']
#         job = Job.jobs.get(id= id)
#         try:
#             favourites= Favourites.objects.get(
#                 user =self.request.user
#                 )
#         except Favourites.DoesNotExist:
#             favourites= Favourites(
#                 user =self.request.user
#                 ) 
#         favourites.favourite_jobs.add(job)
#         return Response({'message': "Job successfully added to your Favourites"}, status=status.HTTP_200_OK)        
        
#     def delete(self, request):
#         id = request.data['id']
#         job = Job.jobs.get(id= id)
        
#         favourites= Favourites.objects.get(
#             user = self.request.user)
        
#         favourites.favourite_jobs.remove(job)
#         return Response({'message': "Job successfully removed from your Favourites"}, status=status.HTTP_200_OK)

