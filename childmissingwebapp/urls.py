from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index1,name='index1'),
    path('home1/',views.home1,name='home1'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('update/',views.update,name='update'), 
    path('adminhome/',views.adminhome,name='adminhome'),
    path('adminlog/',views.adminlog,name='adminlog'),
    path('userlist/',views.userlist,name='userlist'),
    path('deleteuser/<int:uid>/',views.deleteuser,name='deleteuser'),
    path('newcase/',views.newcase,name='newcase'),
   path('caselist/', views.NewCase_list, name='caselist'),
    path('listcase/',views.listcase,name='listcase'),
    path('reportcase/', views.reportcase, name='reportcase'),
    path('verification/', views.verification, name='verification'),
    path('accept_case/<int:case_id>/', views.accept_case, name='accept_case'),
    path('listcase/', views.listcase, name='listcase'),
    path('NewCase_list/', views.NewCase_list, name='NewCase_list'),
    path('deletecase/<int:uid>/<str:model_type>/', views.deletecase, name='deletecase'),
    path('feedback/', views.feedback, name='feedback'),
    path('view_feedback/', views.view_feedback, name='view_feedback'),
    # path('face_comparison/', views.face_comparison_view, name='face_comparison_view'),

    path('detect-face/', views.detect_face, name='detect_face'),

    path('add_recovery_case/', views.add_recovery_case, name='add_recovery_case'),
    path('view_childrecovery/', views.view_childrecovery, name='view_childrecovery'),
    path("detect_child/", views.detect_child_from_video, name="detect_child"),
    path("upload_post/", views.upload_post, name="upload_post"),
    path("posts/", views.view_posts, name="view_posts"),
    path('report/', views.report, name='report'),

    # Analytics and Tip Management
    # path('report/', views.reports, name='report'),
    # path('tips/', views.tips, name='tips'),
    # path('tips/delete/<int:tip_id>/', views.delete_tip_view, name='delete_tip'),
    # path('tips/request_info/', views.request_info_view, name='request_info'),
    # path('child_recovered/<int:new_case_id>/<int:child_locator_id>/', views.child_recovered, name='child_recovered'),
]

