from django.http import JsonResponse
import jpype
import json


# conversation start
def keyboard(request):
    return JsonResponse({
        'type': 'buttons',
        'buttons': ['시작하기', '도움말'] # start button for user
    })

def message(request):
    start = check_is_start(return_str)  # check is start state

    # if start button check
    if start:
        result = list(Maker.objects.values_list('makerName', flat=True))
        return JsonResponse({
            'message': {
                'text': "얼마고를 시작합니다. 핸드폰 기종을 선택하여 주세요!",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': result,
            },
        })

    elif help:
        return JsonResponse({
            'message': {
                'text': "하월은 韓World의 약자로 한국에서 세계로 나가고자 하는 의미가 담겨있습니다. " +
                        "하월은 사회초년생의 최적의 전세 상품을 찾아드리고 그와 같은 월세가격을 측정합니다.",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['시작하기', '도움말']
            },
        })

# user input is start button check
def check_is_start(str):
    if str == "시작하기":
        return True
    else:
        return False

# user input is help button check
def check_is_help(str):
    if str == "도움말":
        return True
    else:
        return False
