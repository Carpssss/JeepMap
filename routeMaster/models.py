# models.py

from django.db import models

class Route(models.Model):
    route_id = models.CharField(max_length=50, unique=True, blank=True)
    route_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.route_id:
            # Get the last route with a valid route_id starting with 'route'
            last_route = Route.objects.exclude(route_id='').order_by('-id').first()
            if last_route and last_route.route_id.startswith('route'):
                try:
                    last_num = int(last_route.route_id.replace('route', ''))
                except ValueError:
                    last_num = 0
            else:
                last_num = 0

            new_num = last_num + 1
            self.route_id = f"route{new_num:03d}"  # Example: route001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.route_id} - {self.route_name}"




class Stop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    name = models.CharField(max_length=255)
    fare_from_base = models.DecimalField(max_digits=6, decimal_places=2)  # <--- ADD THIS


    def __str__(self):
        return f"{self.name} ({self.route.route_name})"


class Fare(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='fares')
    from_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='from_fares')
    to_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='to_fares')
    fare = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.from_stop.name} → {self.to_stop.name}: {self.fare}"
