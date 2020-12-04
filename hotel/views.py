from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Room, Booking, RoomCategory
from .forms import AvailabilityForm
from hotel.booking_functions.availability import check_availability
from hotel.booking_functions.find_total_room_charge import find_total_room_charge
from django.contrib.auth.decorators import login_required

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import environ

import stripe
stripe.api_key = 'sk_test_51Hu0AzH60lA1oSoomphzz4KWIOkf3fyNb6xKnMTLtZuqrYsafvJvMOQXhqxqOV0vy7EkWSuJxV3GxH5q899R8M8l00MDvjRsHl'

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env()


# Create your views here.

class BookingFormView(View):
    def get(self, request, *args, **kwargs):
        print([(x.category, x.category) for x in RoomCategory.objects.all()])
        form = AvailabilityForm()
        if self.request.user.is_anonymous:
            print('anonymous')
        return render(request, 'booking_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            total_room_charge = find_total_room_charge(self.request,
                                                       data['check_in'], data['check_out'], data['room_category'])
            if self.request.user == 'AnonymousUser':
                print('fucker')
            return CheckoutView(self.request, total_room_charge, data['room_category']+' Suite')
        print('user=', self.request.user)

        return HttpResponse('form not valid')


def RoomListView(request):
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    room_values = room_categories.values()
    room_list = []

    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('hotel:RoomDetailView', kwargs={
                           'category': room_category})

        room_list.append((room, room_url))
    context = {
        "room_list": room_list,
    }
    return render(request, 'room_list_view.html', context)


class BookingListView(ListView):
    model = Booking
    template_name = "booking_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list

    # def get_context_data(self, **kwargs):
    #     room = Room.objects.all()[0]
    #     room_categories = dict(room.ROOM_CATEGORIES)
    #     context = super().get_context_data(**kwargs)
    #     context


class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        print(self.request.user)
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)

        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            context = {
                'room_category': room_category,
                'form': form,
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]

            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            message = Mail(
                from_email='dhabaledarshan@gmail.com',
                to_emails='dhabalekalpana@gmail.com',
                subject='Sending from hotelina',
                html_content='<strong>Sending from hotelina</strong>')
            try:
                sg = SendGridAPIClient(env.str('SG_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
                print('SENT!!!')
            except Exception as e:
                print(e)
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of rooms are booked!! Try another one')


class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('hotel:BookingListView')


@login_required
def CheckoutView(request, amount, product_name):
    try:
        stripe.api_key = 'sk_test_51Hu0AzH60lA1oSoomphzz4KWIOkf3fyNb6xKnMTLtZuqrYsafvJvMOQXhqxqOV0vy7EkWSuJxV3GxH5q899R8M8l00MDvjRsHl'
        checkout_session = stripe.checkout.Session.create(
            success_url="http://127.0.0.1:8000/success",
            cancel_url="http://127.0.0.1:8000/cancel",
            payment_method_types=["card"],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(amount)*100,
                        'product_data': {
                            'name': product_name,

                        },
                    },
                    'quantity': 1
                },

            ],
            mode="payment",
        )
        context = {
            'checkout_id': checkout_session.id,
            'product_name': product_name,
            'amount': amount,
            'product_image': '',
        }
        return render(request, 'checkout.html', context)
    except Exception as e:
        return render(request, 'failure.html', {'error': e})


def success_view(request):

    return render(request, 'success.html')


def cancel_view(request):
    return render(request, 'cancel.html')
