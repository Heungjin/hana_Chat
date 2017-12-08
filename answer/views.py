# coding=utf-8
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from answer.models import LoanGoods
import json

button_list = ['시작하기', '전세상품 랭킹', '모든 전세상품', '임대주택정보', '내기', '도움말']

LoanGoodsList = list(LoanGoods.objects.values_list('loan_good_name', flat=True))[2:5]
LoanAllList = list(LoanGoods.objects.values_list('loan_good_name', flat=True))
# test_LoanAllList = list(LoanGoods.objects.values_list('loan_good_name', flat=True).filter(loan_repayment=1)) # 필터링
test_ranking = list(LoanGoods.objects.values_list('loan_good_name', flat=True).order_by('-chat_recommend'))
test_ranking_Str = "\n".join(test_ranking).decode('utf-8')
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
    rankAll = check_is_rankAll(return_str)  # ranking
    rental = check_is_rental(return_str)  # rental
    gamble = check_is_gamble(return_str)  # gamble
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
                'text': "가장 인기있는 전세자금대출 상품 랭킹입니다. 현재 순위는 다음과 같습니다. " + test_ranking_Str ,
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': test_ranking # DB에 넣어서 list로 출력
            },
        })

    elif rankAll:
        return JsonResponse({
            'message': {
                'text': "가장 인기있는 전세자금대출 상품 랭킹입니다.",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': LoanAllList # DB에 넣어서 list로 출력
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
                'buttons': button_list
            },
        })

    elif rental:
        return JsonResponse({
            'message': {
                'text': "크롤링을 통해 가장 최신의 임대주택정보를 화면에 출력 예정",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['나가기']
            },
        })
    elif gamble:
        return JsonResponse({
            'message': {
                'text': "헌기가 걸렸습니다.",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['나가기']
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
def check_is_start(str):
    if str == ("시작하기").decode('utf-8'):
        return True
    else:
        return False


# user input is start button check
def check_is_ranking(str):
    if str == ("전세상품 랭킹").decode('utf-8'):
        return True
    else:
        return False


# user input is start button check
def check_is_rankAll(str):
    if str == ("모든 전세상품").decode('utf-8'):
        return True
    else:
        return False


# user input is help button check
def check_is_help(str):
    if str == ("도움말").decode('utf-8'):
        return True
    else:
        return False


# user input is help button check
def check_is_rental(str):
    if str == ("임대주택정보").decode('utf-8'):
        return True
    else:
        return False

# user input is gamble button check
def check_is_gamble(str):
    if str == ("내기").decode('utf-8'):
        return True
    else:
        return False
