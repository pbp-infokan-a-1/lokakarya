from django.shortcuts import render
from .models import Toko

def toko_list(request):
    toko_list = Toko.objects.all()
    return render(request, 'storepage.html', {'toko_list': toko_list})