# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Route, Stop

def route_list(request):
    routes = Route.objects.all()
    return render(request, 'routeMaster_list.html', {'routes': routes})

def route_create(request):
    if request.method == 'POST':
        route_name = request.POST.get('route_name')
        stops = request.POST.getlist('stops[]')
        fares = request.POST.getlist('fares[]')

        route = Route.objects.create(route_name=route_name)

        for stop_name, fare in zip(stops, fares):
            Stop.objects.create(route=route, name=stop_name, fare_from_base=fare)

        return redirect('fare_matrix', route_id=route.id)

    return render(request, 'routeMaster_form.html')


def fare_matrix(request, route_id):
    route = Route.objects.get(id=route_id)
    stops = list(route.stops.all())
    size = len(stops)

    # Build fare matrix (symmetric)
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                fare = 15
            else:
                distance = abs(i - j)
                if distance <= 4:
                    fare = 15
                else:
                    fare = 15 + ((distance - 4) * 2.20)
            row.append(round(fare, 2))
        matrix.append(row)

    zipped_matrix = zip(stops, matrix)
    return render(request, 'routeMaster_detail.html', {
    'route': route,
    'stops': stops,
    'zipped_matrix': zipped_matrix
})

def route_delete(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    if request.method == 'POST':
        route.delete()
        return redirect('route_list')
    return render(request, 'routeMaster_confirmdelete.html', {'route': route})