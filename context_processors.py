from articles.models import *


def variable_to_base(request): 
    context = {
        'themes': Theme.objects.all(),
        'regions': Region.objects.all(),
    }
    return context