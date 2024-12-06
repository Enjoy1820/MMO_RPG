from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Response, NewsletterSubscription
from rest_framework.generics import get_object_or_404

from .forms import AdForm, ResponseForm, NewsletterSubscriptionForm
from .models import Ad


def ad_list(request):
    ads = Ad.objects.all()
    return render(request, 'ad_list.html', {'ads': ads})

def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'ad_form.html', {'form': form})

def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ad_confirm_delete.html', {'ad': ad})



@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'ad_form.html', {'form': form})

@login_required
def ad_edit(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ad_form.html', {'form': form})


@login_required
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    responses = ad.responses.all()  # Получаем все отклики на объявление

    if request.method == 'POST':
        response_form = ResponseForm(request.POST)
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.ad = ad  # Привязываем отклик к объявлению
            response.user = request.user  # Привязываем отклик к текущему пользователю
            response.save()

            subject = f'Новый отклик на ваше объявление: {ad.title}'
            message = f'Пользователь {request.user.username} оставил отклик: {response.text}'
            recipient_list = [ad.author.email]
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

            return redirect('ad_detail', ad_id=ad.id)
    else:
        response_form = ResponseForm()

    return render(request, 'ad_detail.html', {
        'ad': ad,
        'responses': responses,
        'response_form': response_form,
    })


def my_responses(request):
    ads = Ad.objects.filter(author=request.user)
    responses = Response.objects.filter(ad__in=ads)

    if request.method == 'POST':
        if 'delete' in request.POST:
            response_id = request.POST.get('response_id')
            response = get_object_or_404(Response, id=response_id)
            response.delete()
            return redirect('my_responses')

        if 'accept' in request.POST:
            response_id = request.POST.get('response_id')
            response = get_object_or_404(Response, id=response_id)
            response.accepted = True
            response.save()


            subject = f'Ваш отклик на объявление "{response.ad.title}" принят!'
            message = f'Ваш отклик: "{response.text}" был принят.'
            recipient_list = [response.author.email]
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

            return redirect('my_responses')

    return render(request, 'my_responses.html', {'responses': responses})


def responce_create(request, ad_id):
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            respons = form.save()
            respons.user = request.user
            respons.ad = Ad.objects.get(id=ad_id)
            respons.save()
            return redirect('ad_list')
    else:
        form = ResponseForm()
    return render(request, 'ad_form.html', {'form': form})


def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscription_success')
    else:
        form = NewsletterSubscriptionForm()
    return render(request, 'subscribe.html', {'form': form})


def send_newsletter(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        subscribers = NewsletterSubscription.objects.all()
        recipient_list = [subscriber.email for subscriber in subscribers]

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

        return redirect('newsletter_sent')

    return render(request, 'send_newsletter.html')