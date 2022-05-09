from django.views.generic import ListView
from rooms.models import Room


class HomeView(ListView):
    """HomeView Definition"""

    template_name = "home.html"
    model = Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
