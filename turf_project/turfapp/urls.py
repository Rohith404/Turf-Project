from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-turf/', views.AddTurf.as_view(), name = 'add_turf'),
    path('turf-list/', views.TurfListView.as_view(), name = 'turf_list'),
    path('turf/<int:pk>/', views.TurfView.as_view(), name = 'turf_detail'),
    path('book/<int:turf_id>/', views.TrufBookView.as_view(), name = 'booking'),
    path('bookings/', views.OwnerTurfBookingsView.as_view(), name = 'bookings'),
    path('bookings/<int:pk>/', views.BookingSuccessView.as_view(), name = "booking-detail"),
    path('my-bookings/', views.UserTurfBookingsView.as_view(), name= 'my-bookings'),
    path('check-availablity/', views.check_booking_availability, name = 'check-availability'),
    path('details/', views.createpost, name='details'),
    path('show/', views.showvideo, name='show')
]