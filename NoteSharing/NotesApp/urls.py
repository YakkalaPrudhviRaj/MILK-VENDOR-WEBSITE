from django.urls import path
from NotesApp import views
from django.contrib.auth import views as v

urlpatterns = [
	path('',views.home,name="hm"),
	path('abt/',views.about,name="ab"),
	path('cnt/',views.contact,name="ct"),
	path('reg/',views.register,name="rg"),
    path('login/',v.LoginView.as_view(template_name="notehtmls/login.html"),name="lg"),
	path('logout/',v.LogoutView.as_view(template_name="notehtmls/logout.html"),name="lgo"),
    path('roles/',views.rolechange,name="role"),
    path('roleup/<int:t>/',views.roleupdate,name="rolup"),
    path('pfle/',views.profile,name="pf"),
    path('uppf/',views.updateprofile,name="uppfle"),
    path('notes/',views.noteslist,name="ntlist"),
    path('notesStudent/',views.notesliststudent,name="ntlists"),
    path('payment/<int:id>/',views.payment,name="payment"),
    path('notes/edit/<int:id>/', views.edit_note, name="edit_note"),
    path('notes/delete/<int:id>/', views.delete_note, name="delete_note"),
    path('merchantlist/', views.merchantList, name='mlist'),
    path('doctors/', views.doctorlist, name='dlist'),
    path('orders/', views.order_list, name='olist')
]