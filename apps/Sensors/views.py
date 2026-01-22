from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Sensor
from .forms import SensorForm

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def sensor_list_view(request):
    sensors = Sensor.objects.all()
    return render(request, 'sensor_list.html', {'sensors': sensors})

@user_passes_test(is_admin)
def sensor_create_view(request):
    if request.method == 'POST':
        form = SensorForm(request.POST) # или request.POST
        if form.is_valid():
            sensor = form.save(commit=False)
            sensor.owner = request.user # Привязываем админа как владельца
            sensor.save()
            return redirect('sensor_list')
    else:
        form = SensorForm()
    return render(request, 'sensor_form.html', {'form': form})

@user_passes_test(is_admin)
def sensor_delete_view(request, pk):
    sensor = get_object_or_404(Sensor, pk=pk)
    sensor.delete()
    return redirect('sensor_list')