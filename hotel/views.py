from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
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


import datetime
import json


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
        if "check_in" in request.session:
            s = request.session
            form_data = {
                "check_in": s['check_in'], "check_out": s['check_out'], "room_category": s['room_category']}
            # booking_form_data = self.request.session['booking_form_data']
            # booking_form_data = dict(booking_form_data)
            # form_data2 = {
            #     "check_in": "2021-01-01T20:27:00+00:00",
            #     "check_out": "2021-01-02T20:27:00+00:00",
            #     "room_category": "NON-AC"
            # }
            form = AvailabilityForm(request.POST or None, initial=form_data)
            print(form)
        else:
            form = AvailabilityForm()
        return render(request, 'booking_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            print('data_from_form = ', data)

            total_room_charge = find_total_room_charge(self.request,
                                                       data['check_in'], data['check_out'], data['room_category'])
            if self.request.user.is_anonymous:
                # def default(o):
                #     if isinstance(o, (datetime.date, datetime.datetime)):
                #         return o.strftime("%Y-%m-%dT%H:%M")

                # def jsonify_datetime(d):
                #     return json.dumps(
                #         d,
                #         sort_keys=True,
                #         indent=1,
                #         default=default
                #     )

                print('storing_in_session =>', data['check_in'].strftime(
                    "%Y-%m-%dT%H:%M"), data['check_out'].strftime("%Y-%m-%dT%H:%M"), data['room_category'])

                self.request.session['check_in'] = data['check_in'].strftime(
                    "%Y-%m-%dT%H:%M")
                self.request.session['check_out'] = data['check_out'].strftime(
                    "%Y-%m-%dT%H:%M")
                self.request.session['room_category'] = data['room_category'].category

                return redirect(reverse('account_login'))
            return CheckoutView(self.request, total_room_charge, data['room_category'].category+' Suite')
        return HttpResponse('form not valid', form.errors)


# def RoomListView(request):
#     room = Room.objects.all()[0]
#     room_categories = dict(room.ROOM_CATEGORIES)
#     room_values = room_categories.values()
#     room_list = []

#     for room_category in room_categories:
#         room = room_categories.get(room_category)
#         room_url = reverse('hotel:RoomDetailView', kwargs={
#                            'category': room_category})

#         room_list.append((room, room_url))
#     context = {
#         "room_list": room_list,
#     }
#     return render(request, 'room_list_view.html', context)


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


def contact_us(request):
    return render(request, 'contact_us.html')
