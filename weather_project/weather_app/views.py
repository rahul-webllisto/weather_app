from django.shortcuts import render
import requests
from django.contrib import messages
from . models import City
from . forms import CityForm
# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=686fe935f441f72b41019aa7cc8ea05a'
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data.get('name').strip()
            data = requests.get(url.format(city_name)).json()
            if City.objects.filter(name=city_name).exists():
                pass            
            elif data.get('message'):
                messages.error(request,'Please enter a valid City name')
            else:    
                new_city = City.objects.create(name=city_name)
                new_city.save()
            form.cleaned_data['name'] = None
            form = CityForm()
    else:
        form = CityForm()
    cities = City.objects.all().order_by('-pk')
    weather_data = []
    for city in cities:            
        city_weather = requests.get(url.format(city)).json()                      
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }             
        weather_data.append(weather) 
    messages.error(request, 'Please enter a valid City name')       
    context={'weather_data': weather_data, 'form': form}
    return render(request, 'index.html',context)
