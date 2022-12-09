from audioop import reverse
import razorpay
from django.contrib.auth import authenticate, login
# from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .forms import *
from . import models
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.conf import settings
# Create your views here.
from django.contrib import messages
from .models import Post

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        
        user_form=UserForm(request.POST)

        if user_form.is_valid():
            user=user_form.save()
            user.save()
            # print(user_form.cleaned_data)
            address = user_form.cleaned_data.get('address')
            gender = user_form.cleaned_data.get('select_gender')
            is_owner = user_form.cleaned_data.get('are_you_turf_owner')
            profile = models.Profile.objects.create(
                user = user,
                address = address,
                gender = gender,
                is_owner = is_owner,
            )
            print(profile)

            messages.success(request,'Thank You For Registering')
            return redirect('index')
            #return render(request,'register.html',context={'user_form':user_form,'message':'Registration Success'})

        else:
            HttpResponse('invalid form')
    else:
        user_form=UserForm()
        #profile_form=ProfileForm()
       
    return render(request,'register.html',context={'user_form':user_form})
    


def userlogin(request):
    if request.method=='POST':
        form=AuthenticationForm(request, data=request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                if user.profile.is_owner:
                    messages.success(request, "You're owner!")
                login(request,user)
                return redirect('dashboard')
            else:
                return HttpResponse('not active')
        else:
            messages.error(request,'invalid username or password')
            return redirect('login')


    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})


def logout(request):
    auth_logout(request)
    return render(request,"index.html")

def dashboard(request):
    return render(request,"dashboard.html")


class AddTurf(LoginRequiredMixin, FormView):
    form_class = TurfForm
    template_name = 'turf/add_turf.html'
    success_url = reverse_lazy('add_turf')

    def get_success_url(self):
        return reverse_lazy('turf_detail', kwargs = {'pk': self.object.id})

    def get_initial(self):
        intials =  super().get_initial()
        intials.update({
            'owner': self.request.user,
        })
        return intials
       
    def form_valid(self, form):
        self.object = form.save()
        images = self.request.FILES.getlist('image')
        for img in images:
            t_image = models.TurfImages.objects.create()
            t_image.image.save(img.name, img)
            self.object.images.add(t_image)
            self.object.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class TurfView(LoginRequiredMixin, DetailView):
    model = models.Turf
    template_name = 'turf/turf_detail.html'


class TurfListView(LoginRequiredMixin, ListView):
    model = models.Turf
    template_name = 'turf/turf_list.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        self.object_list = models.Turf.objects.filter(name__icontains = name)
        context = self.get_context_data()
        return self.render_to_response(context)

def check_booking_availability(request):
    turf_id = request.GET.get('turf_id')
    turf = models.Turf.objects.get(id = turf_id)
    available_bookings_on_this_day = models.Bookings.objects.filter(date = request.GET.get('date'), turf = turf)
    already_booked_slot  = available_bookings_on_this_day.filter(time_from = request.GET.get('time_from'))
    length_of_booked_slot = len(already_booked_slot)
    if(length_of_booked_slot == 0):
        return HttpResponse("ok")
    else:
        return HttpResponse("failed")


class BookingSuccessView(LoginRequiredMixin, DetailView):
    model = models.Bookings
    template_name = 'turf/booking_details.html'

class TrufBookView(LoginRequiredMixin, FormView):
    form_class = BookingForm
    template_name = 'turf/booking_form.html'
    success_url = reverse_lazy('turf_list')

    def get_success_url(self) -> str:
        return reverse_lazy('booking-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        turf_id = self.kwargs.get('turf_id')
        turf = models.Turf.objects.get(id = turf_id)
        available_bookings_on_this_day = models.Bookings.objects.filter(date = self.request.POST.get('date'),  turf= turf)
        already_booked_slot  = available_bookings_on_this_day.filter(time_from = self.request.POST.get('time_from'))
        length_of_booked_slot = len(already_booked_slot)
        # if(length_of_booked_slot == 0):
        messages.success(self.request, 'Your Booking  submitted')
        self.object = form.save()
        models.notifications.objects.create(
            user = self.object.turf.owner,
            matter = f'New booking form user {self.object.user.username}'
        )
        return super().form_valid(form)
        # else:
        #     raise forms.ValidationError("This time slot is already booked")

    def get_context_data(self, **kwargs):
        client = razorpay.Client(auth = (settings.RAZORPAY_ID, settings.RAZORPAY_SECRET))
        turf = models.Turf.objects.get(id = self.kwargs.get('turf_id'))
        payment = client.order.create(data = {"amount": turf.rent_per_hour * 100, "currency": "INR"})
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'rent': turf.rent_per_hour,
            'order_id': payment['id'],
            'turf_id': self.kwargs.get('turf_id'),
        })
        return ctx

    def get_initial(self):
        intials =  super().get_initial()
        turf = models.Turf.objects.get(id = self.kwargs.get('turf_id'))
        intials.update({
            'user': self.request.user,
            'turf': turf,
        })
        return intials

class OwnerTurfBookingsView(LoginRequiredMixin, ListView):
    """
    this will show turf owner bookings
    """
    template_name = 'turf/turf_booking.html'

    def get_queryset(self):
        return models.Bookings.objects.filter(turf__owner = self.request.user)
        
class UserTurfBookingsView(LoginRequiredMixin, ListView):
    """
    this will show user bookings
    """
    template_name = 'turf/turf_bookings_user.html'

    def get_queryset(self):
        return models.Bookings.objects.filter(user = self.request.user)


def createpost(request):
        if request.method == 'POST':
            if request.POST.get('username')  and request.POST.get('ownername')  and request.POST.get('contact') and request.POST.get('turfdetails') and request.POST.get('complaint'):
                post=Post()
                post.username= request.POST.get('username')
                post.ownername= request.POST.get('ownername')
                post.contact= request.POST.get('contact')
                post.turfdetails= request.POST.get('turfdetails')
                post.complaint= request.POST.get('complaint')
                post.save()
                
                return render(request, 'turf/details.html')  

        else:
                return render(request,'turf/details.html')


def showvideo(request):
     alldata= Post.objects.all()
     context={'Post':alldata}
     return render(request,'turf/show.html',context)


