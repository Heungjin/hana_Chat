# coding=utf-8
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from answer.models import LoanGoods
import json

button_list = ['시작하기', '모든 전세상품(랭킹순)', '임대주택정보', '내기', '도움말']

LoanGoodsList = list(LoanGoods.objects.values_list('loan_good_name', flat=True))[2:5]
LoanAllList = list(LoanGoods.objects.values_list('loan_good_name', flat=True))
# test_LoanAllList = list(LoanGoods.objects.values_list('loan_good_name', flat=True).filter(loan_repayment=1)) # 필터링
test_ranking = list(LoanGoods.objects.values_list('loan_good_name', flat=True).order_by('-chat_recommend'))
test_ranking_Str = "\n".join(test_ranking).encode('utf8')
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
    rental = check_is_rental(return_str)  # rental
    gamble = check_is_gamble(return_str)  # gamble
    help = check_is_help(return_str)  # help
    goods = check_is_goods(return_str)
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
                'text': "가장 인기있는 전세자금대출 상품 랭킹입니다. 현재 순위는 다음과 같습니다. \n" + test_ranking_Str,

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

    elif goods:
        loanGoods = LoanGoods.objects.get(loan_good_name=(return_str).encode('utf-8'))
        # loanGoodsDesc = list(LoanGoods.objects.filter(chatbot_description=loanGoods))

        # list(LoanGoods.objects.values_list('loan_good_name', flat=True).filter(loan_repayment=1))[0]
        return JsonResponse({
            'message': {
                'text': (return_str).encode('utf-8') + "을 선택하였습니다. \n" +
                (return_str).encode('utf-8') + "의 정보는 다음과 같습니다." + (loanGoods.chatbot_description).encode('utf-8'),
                "photo": {
                    "url": "hana-finance.c7qldhnfrqvy.ap-northeast-2.rds.amazonaws.com:3306" + (loanGoods.chatbot_img).encode('utf-8'),
                    "width": 640,
                    "height": 480
                }
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': button_list
            },
        })



    # elif model:
    #     phoneModel = PhoneModel.objects.get(modelName=return_str)
    #     User.setUserState(user_key, phoneModel)
    #     return JsonResponse({
    #         'message': {
    #             'text': return_str + "을 구매하길 원하신다면 '가격 정보 보기'를, 판매하길 원하신다면 '모의 판매글 올리기'를 선택해주세요.",
    #             "photo": {
    #                 "url": "http://ec2-13-124-156-121.ap-northeast-2.compute.amazonaws.com:8000" + phoneModel.modelPhoto.url,
    #                 "width": 640,
    #                 "height": 480
    #             },
    #         },
    #         'keyboard': {
    #             'type': 'buttons',
    #             'buttons': ['가격 정보 보기', '모의 판매글 올리기'],
    #         },
    #     })

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

# user input is maker button check
def check_is_goods(str):
    goods = LoanGoods.objects.values_list('loan_good_name', flat=True)
    if str in goods:
        return True
    else:
        return False
