from .models import Substation

def add_substations_to_context(request):
    return {
        'model_sub_data': Substation.objects.all().order_by('id')
    }
