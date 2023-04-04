from django.http import HttpResponse
from django.shortcuts import render
import pricecheck.scraper as scraper
from django.template import loader

def index(request):
    return render(request, 'pricecheck/index.html')

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        page = request.POST['page']
        print(search, page)
        data = scraper.get_data(search, page)
        return render(request, 'pricecheck/index.html', {'data': data})

