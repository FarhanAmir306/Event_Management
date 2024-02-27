from django.urls import path
from . import views

urlpatterns = [
    # path('create/',views.AddCreateView.as_view(),name='add_event'),
    path('list/',views.EventList.as_view(),name='list'),
    path('accept/<int:id>/',views.attendent_event,name='accept'),
    # path('decline/<int:id>/',views.EventDelete.as_view(),name='decline'),
    path('decline/<int:id>/',views.attendent_decline,name='decline'),
    path('details/<int:id>/',views.EventDetailsView.as_view(),name='details'),
    path('edit_profile/',views.ProfileUpdate.as_view(),name='edit_profile'),
    # path('password_change/',views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/',views.password_reset_by_user,name='password_change'),

    path('profile_category/', views.profile, name='profile'),
    path('profile_category/<slug:category_slug>/', views.profile, name='category_wise'),
    path('delete/<int:id>/',views.TaskDelete,name='remove'),
    path('comments/<int:pk>/',views.PostView.as_view(),name='comment'),

    path('editComment/<int:id>/<int:post_id>/',views.edit_comment,name='editcomment'),
    path('deleteComment/<int:id>/<int:post_id>/',views.delete_comment,name='deletecomment'),
    
]
