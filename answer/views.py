# coding=utf-8
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from answer.models import LoanGoods
import json

button_list = ['시작하기', '모든 전세상품(랭킹순)', '실시간 통계보기', '우리는 하월이다', '도움말']
stat_list = ['웹에서 가장 많이 추천된 상품','고객 나이대별 통계', '고객 연봉별 통계']
LoanGoodsList = list(LoanGoods.objects.values_list('loan_good_name', flat=True))[2:5]
LoanAllList = list(LoanGoods.objects.values_list('loan_good_name', flat=True))
# test_LoanAllList = list(LoanGoods.objects.values_list('loan_good_name', flat=True).filter(loan_repayment=1)) # 필터링

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
    rankAll = check_is_rankAll(return_str)  # ranking

    stat = check_is_stat(return_str)  # stat
    stat_age = check_is_stat_age
    stat_recommend = check_is_stat_recommend
    stat_salary = check_is_stat_salary
    help = check_is_help(return_str)  # help
    goods = check_is_goods(return_str)
    test_ranking = list(LoanGoods.objects.values_list('loan_good_name', flat=True).order_by('-chat_recommend'))
    test_ranking_Str = "\n * ".join(test_ranking).encode('utf8')

    # if start button check
    print(return_str)
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

    elif rankAll:
        return JsonResponse({
            'message': {
                'text': "가장 인기있는 전세자금대출 상품 랭킹입니다. 현재 순위는 다음과 같습니다. \n * " + test_ranking_Str,

            },
            'keyboard': {
                'type': 'buttons',
                'buttons': test_ranking # DB에 넣어서 list로 출력
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

    elif stat:
        return JsonResponse({
            'message': {
                'text': "실시간 통계를 보여주는 통계페이지 입니다. 버튼을 눌러 결과를 확인하세요.",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': stat_list
            },
        })

    elif stat_age:
        return JsonResponse({
            'message': {
                'text': "stat_age",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': stat_list
            },
        })


    elif stat_recommend:
        return JsonResponse({
            'message': {
                'text': "stat_recommend",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': stat_list
            },
        })


    elif stat_salary:
        return JsonResponse({
            'message': {
                'text': "stat_salary",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': stat_list
            },
        })



    elif goods:
        loanGoods = LoanGoods.objects.get(loan_good_name=(return_str).encode('utf-8'))
        loanGoods.chat_recommend = loanGoods.chat_recommend + 1
        loanGoods.save()
        # loanGoodsDesc = list(LoanGoods.objects.filter(chatbot_description=loanGoods))

        # list(LoanGoods.objects.values_list('loan_good_name', flat=True).filter(loan_repayment=1))[0]
        return JsonResponse({
            'message': {
                "photo": {
                    "url": "http://13.124.236.32:8000" + loanGoods.chatbot_img.url,
                    "width": 640,
                    "height": 480
                },
                'text': (return_str).encode('utf-8') + "의 정보는 다음과 같습니다.\n" + (loanGoods.chatbot_description).encode('utf-8') +
                "\n 카톡 추천수 : " + str(loanGoods.chat_recommend) + "번",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': button_list
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
def check_is_rankAll(str):
    if str == ("모든 전세상품(랭킹순)").decode('utf-8'):
        return True
    else:
        return False


# user input is help button check
def check_is_help(str):
    if str == ("도움말").decode('utf-8'):
        return True
    else:
        return False


# user input is gamble button check
def check_is_stat(str):
    if str == ("실시간 통계보기").decode('utf-8'):
        return True
    else:
        return False


def check_is_stat_age(str):
    if str == ("고객 나이대별 통계").decode('utf-8'):
        return True
    else:
        return False


def check_is_stat_recommend(str):
    if str == ("웹에서 가장 많이 추천된 상품").decode('utf-8'):
        return True
    else:
        return False


def check_is_stat_salary(str):
    if str == ("고객 연봉별 통계").decode('utf-8'):
        return True
    else:
        return False

# user input is maker button check
def check_is_goods(str):
    goods = LoanGoods.objects.values_list('loan_good_name', flat=True)
    if str in goods:
        return True
    else:
        return False
