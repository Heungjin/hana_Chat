from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# conversation start
def keyboard(request):
    return JsonResponse({
        'type': 'buttons',
        'buttons': ['1', '2'] # start button for user
    })
@csrf_exempt
def message(request):
    # if start button check
        return JsonResponse({
            'message': {
                'text': "1",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['1', '2']
            },
        })



# user input is start button check
def check_is_start(str):
    if str == "1":
        return True
    else:
        return False

# user input is help button check
def check_is_help(str):
    if str == "2":
        return True
    else:
        return False
