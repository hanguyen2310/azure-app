from django.http import HttpResponse
from django.shortcuts import render
import ebay.scraper as scraper
from django.template import loader

def index(request):
    return render(request, 'ebay/index.html')

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        data = scraper.get_data(search)
        return render(request, 'ebay/index.html', {'data': data})



