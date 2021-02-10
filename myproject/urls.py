"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.urls import path, re_path
from django.conf.urls import include, url
from machines import views
from accounts import views as accounts_views
#from machines.views import consupt_works
#from machines.views import delete
from django.conf import settings
from django.conf.urls.static import static




#from .views import HomeView, get_data, ChartData





urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
    path('ncompany/', views.new_company, name='ncompany'),
    path('supervisor_reg/', views.supervisor_reg, name='supervisor_reg'),
    path('admin/', admin.site.urls),
    path('signup/', accounts_views.signup,  name='signup'),
    path('techleader_reg/', views.techleader_reg),
    path('machine_reg/', views.machine_reg),
    path('driver_reg/', views.driver_reg),
    path('techleader_pult/', views.techleader_pult, name='techleader_pult'),
    path('supervisor_pult/', views.supervisor_pult, name='supervisor_pult'),
    path('driver_pult/', views.driver_pult),
    path('response_pult/', views.response_pult, name='response_pult'),
    #path('success', success, name = 'success'),
    path('simpleemail/<emailto>', views.sendSimpleEmail, name = 'sendSimpleEmail'),
    path('htmlemail/<emailto>', views.sendHTMLEmail, name = 'sendHTMLEmail'),
    #patterns('myapp.views', url(r'^simpleemail/(?P<emailto>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/',  'sendSimpleEmail' , name = 'sendSimpleEmail'),)
    #url(r'^simpleemail/(?P<emailto>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/',  'sendSimpleEmail' , name = 'sendSimpleEmail')
    path('password_ch/', views.password_ch, name='password_ch'),
    path('forgot_passw/', views.forgot_passw, name='forgot_passw'),
    path('respons_reg/', views.respons_reg),
    #path('respons_pult/', views.respons_pult),
    #path('driver_reg/<name>&<compId>', views.driver_reg),
    #path('driver_pult/', views.driver_pult),
    path('machine_reg/<name>&<compId>', views.driver_reg),
    #path('consupt_works/', consupt_works.as_view(), name='consupt_works'),
    path('consupt_works/', views.consupt_works, name='consupt_works'),
    path('chart/', views.chart, name='chart'),
    path('consupt_works2/', views.consupt_works2, name='consupt_works2'),
    path('chart2/', views.chart2, name='chart2'),
    path('consupt_works3/', views.consupt_works3, name='consupt_works3'),
    path('chart_oil/', views.chart_oil, name='chart_oil'),
    path('lead_samples/', views.lead_samples, name='lead_samples'),
   
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
