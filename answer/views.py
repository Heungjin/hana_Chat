from django.http import JsonResponse
import json


# conversation start
def keyboard(request):
    return JsonResponse({
        'type': 'buttons',
        'buttons': ['1', '2'] # start button for user
    })

def message(request):
    message = ((request.body).decode('utf-8'))

    return_json_str = json.loads(message)
    return_str = return_json_str['content']



    start = check_is_start(return_str)  # check is start state

    # if start button check
    if start:
        return JsonResponse({
            'message': {
                'text': "1",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['1', '2']
            },
        })

    elif help:
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
