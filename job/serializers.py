from django.http import request
from rest_framework import serializers
from .models import Address, Category, Skills
from .models import Job, Proposal, ProposedJobs, JobRequest
from users import serializers as account_serializer
from drf_extra_fields.fields import Base64ImageField


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    # client = account_serializer.ClientAccountSerializer(read_only = True)

    category = serializers.SlugRelatedField(
        read_only=False, 
        slug_field='title',
        queryset= Category.objects.all()
        )
    skills = serializers.SlugRelatedField(
        many = True,
        read_only=False, 
        slug_field='title',
        queryset= Skills.objects.all()
        )
    announced_on = serializers.ReadOnlyField()
    category_image = serializers.ReadOnlyField()
    client_name = serializers.ReadOnlyField()
    proposants = serializers.ReadOnlyField()
    display_status = serializers.ReadOnlyField()
    display_listing_type= serializers.ReadOnlyField()

    class Meta:
        model = Job
        exclude = [ ]
        read_only_fields = ['slug', 'announced_on']
        extra_kwargs = {'price': {'write_only': True}, 'url': {'lookup_field': 'slug'}}

    def validate_client(self, client):
        user = serializers.CurrentUserDefault()
        if client.basic_user != user:
            raise serializers.ValidationError("Lol Nice Try!")
        return client
    
class FavouritesSerializer(serializers.ModelSerializer):
    pass
    # favourite_jobs = JobSerializer(many = True, read_only = True)
    # user = serializers.SlugRelatedField(
    #     read_only=False, 
    #     slug_field='full_name',
    #     queryset= User.objects.all()
    #     )
    # class Meta:
    #     model = Favourites
    #     fields = ['user', 'favourite_jobs', 'added_on']
    #     read_only_fields = ['added_on']
        
class ProposalSerializer(serializers.ModelSerializer):
    job_details = serializers.ReadOnlyField()
    proposant_details = serializers.ReadOnlyField()


    class Meta:
        model = Proposal
        fields = '__all__'
        
class JobRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRequest
        fields = '__all__'
        

class ProposedJobsSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many = True, read_only = True)
    class Meta:
        model = ProposedJobs
        fields = '__all__'




class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    image=Base64ImageField(required= False)
    class Meta:
        model = Category
        fields = '__all__'
