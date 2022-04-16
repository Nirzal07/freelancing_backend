from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.views import APIView
from job import views as jobs_views
from rest_framework.response import Response
from rest_framework import status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('job/', include('job.urls')),
    path('users/', include('users.urls')),
    path('homepage', jobs_views.HomePage.as_view(), name= 'homepage'),
    path('address_list', jobs_views.AddressView.as_view(), name= 'address'),
    path('categories_list', jobs_views.CategoryView.as_view(), name= 'categories'),
    path('skills_list', jobs_views.SkillsView.as_view(), name= 'skills'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

class ApiOverview(APIView):
    
    def get(self, request):
        # populate_db()
        url_list = {
            "Home page"                                         : "/homepage",
            "List of Job Categories"                            : "/categories_list",
            "List of Addresss"                                 : "/districts_list", 
            "Lists of Skills"                                   : "/skills_list",   
  
            "account": {
                'User SignUp'                                   : '/accounts/signup',
                'User SignIn'                                   : '/accounts/signin',
                'SignIn with Google'                            : '/accounts/signin_google',
                'SignUp with Google'                            : '/accounts/signup_google',
                'SignIn with Facebook'                          : '/accounts/signin_facebook',
                'SignUp with Facebook'                          : '/accounts/signup_facebook',
                # 'Get and Update Full Name'                      : '/accounts/basicuser',
                'Create/List of Employer Account'               : '/accounts/employer/',
                'Edit/Retrieve/Delete Employer Account'         : '/accounts/employer/pk/',
                'Create/List Employer Account'                  : '/accounts/jobseeker',
                'Edit/Retrieve/Delete JobSeeker Account'        : '/accounts/jobseeker/pk/',

            },
            
            "jobs":{
                'Create/List of Job Vacancies'                  : '/jobs/vacancies/',
                'Edit/Retrieve/Delete Job Vacancies'            : '/jobs/vacancies/pk',
                'Search Results, Filtering And Ordering URL'    : "/jobs/vacancies/?ordering=+-order_by&page=page_num&search=search&category=cat_1&category=cat_2&min_salary=min_sal&max_salary=max_sal&education=edu_level&experience=exp_level&district=dist_1&district=dist_2",
                'Create/List/Delete of Favourite Jobs'          : '/jobs/favourites',
                'Create/List/Delete of Applied Jobs'            : '/jobs/applied',
                'List of Applicants Jobs'                       : '/jobs/applicants',
                }
        }
        
        return Response(url_list, status=status.HTTP_200_OK)
    
urlpatterns += [path('', ApiOverview.as_view(), name='api_overview')]