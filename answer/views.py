# coding=utf-8
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

button_list = ['시작하기', '전세상품 랭킹', '도움말', '임대주택정보', '뭐먹지?', '내기']


# conversation start
def keyboard(request):
    return JsonResponse({
        'type': 'buttons',
        'buttons': button_list # start button for user
    })


# response to user post type request
@csrf_exempt
def message(request):
    json_raw = ((request.body).decode('utf-8'))
    return_json_str = json.loads(json_raw)
    return_str = return_json_str['content']

    start = check_is_start(return_str)  # start
    ranking = check_is_ranking(return_str)  # ranking
    help = check_is_help(return_str)  # help

    # if start button check
    if start:
        # result = list(Maker.objects.values_list('makerName', flat=True)) 상품
        return JsonResponse({
            'message': {
                'text': "사회초년생에게 맞는 전세자금대출 시작합니다. 대출받으실 금액을 알려주세요!",
            },
            'keyboard': {
                'type': 'text',
            },
        })

    elif ranking:
        return JsonResponse({
            'message': {
                'text': "가장 인기있는 전세자금대출 상품 랭킹입니다.",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['우리은행#1', '신한은행#1', '우리은행#2','우리은행#3','농협#1','기업은행#1']
            },
        })

    elif help:
        return JsonResponse({
            'message': {
                'text': "하월은 사회초년생에게 가장 적합한 맞춤형 전세자금대출 상품을 추천합니다. " +
                        "하월은 사회초년생의 내집마련을 응원합니다.",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['시작하기', '도움말']
            },
        })

    else:
        return JsonResponse({
            'message': {
                'text': "테스트버전이기 때문에 초기화면으로 돌아갑니다.",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': button_list # start button for user
            },
        })


# user input is start button check
def check_is_start(run_start):
    if run_start == "시작하기":
        return True
    else:
        return False


# user input is start button check
def check_is_ranking(str):
    if str == "전세상품 랭킹":
        return True
    else:
        return False


# user input is help button check
def check_is_help(str):
    if str == "도움말":
        return True
    else:
        return False
