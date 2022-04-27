from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('<int:id>/ind_criminal',views.ind_criminal,name='ind_criminal'),
    #path('criminal',views.criminal,name='criminal'),
    #path('crime',views.crime,name='crime'),
    #path('compare_faces',views.compare_faces,name='compare'),
    #path('criminal_form',views.criminal_form,name='criminal_form'),
    #path('testimg_form',views.testimg_form,name='testimg_form'),
    path('failure_detection',views.failure_detection,name='failure_detection'),
]