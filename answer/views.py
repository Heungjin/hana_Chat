# coding=utf-8
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from answer.models import LoanGoods, StatisticAge2, StatisticList2, StatisticLoanAmount2, StatisticSalary2, Banks
import json

button_list = ['시작하기', '모든 전세상품(랭킹순)', '실시간 통계보기', '우리는 하월이다', '도움말']
stat_list = ['웹에서 가장 많이 추천된 상품','고객 나이대별 통계', '고객 연봉별 통계', '가장많이받은 대출액']
LoanGoodsList = list(LoanGoods.objects.values_list('loan_good_name', flat=True))[2:5]
LoanAllList = list(LoanGoods.objects.values_list('loan_good_name', flat=True))

StatAge20to30 = str(list(StatisticAge2.objects.all())[0].m20_30)
StatAge30to40 = str(list(StatisticAge2.objects.all())[0].m30_40)
StatAge40to50 = str(list(StatisticAge2.objects.all())[0].m40_50)
StatAge50to60 = str(list(StatisticAge2.objects.all())[0].m50_60)
StatAge60to = str(list(StatisticAge2.objects.all())[0].m60_0)


#StatAge30to40Bank = Banks.objects.get('bank_name', flat=True).filter(bank_id = list(StatisticAge2.objects.all())[1].m30_40)
StatAge20to30BankNum = list(StatisticAge2.objects.all())[1].m40_50
StatAge30to40BankNum = list(StatisticAge2.objects.all())[1].m40_50
StatAge40to50BankNum = list(StatisticAge2.objects.all())[1].m40_50
StatAge50to60BankNum = list(StatisticAge2.objects.all())[1].m50_60
StatAge60toBankNum = list(StatisticAge2.objects.all())[1].m60_0

StatAge20to30Bank = Banks.objects.get(bank_id = StatAge20to30BankNum)
StatAge30to40Bank = Banks.objects.get(bank_id = StatAge30to40BankNum)


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
    stat_age = check_is_stat_age(return_str)
    stat_recommend = check_is_stat_recommend(return_str)
    stat_salary = check_is_stat_salary(return_str)


    help = check_is_help(return_str)  # help
    goods = check_is_goods(return_str)
    test_ranking = list(LoanGoods.objects.values_list('loan_good_name', flat=True).order_by('-chat_recommend'))
    test_ranking_Str = "\n * ".join(test_ranking).encode('utf8')

    # if start button check
    print(return_str)
    print(StatAge20to30BankNum)
    print(StatAge30to40BankNum)
    print(StatAge20to30Bank.bank_name)
    print(StatAge30to40Bank.bank_name)


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
                'text': "현재 하월의 이용고객은 \n20대 ~ 30대 : " + StatAge20to30 + "명 \n" +
                        "30대 ~ 40대 : " + StatAge30to40 + "명\n40대 ~ 50대 : " + StatAge40to50 + "명 \n" +
                        "50대 ~ 60대 : " + StatAge50to60 + "명\n60대 이상 : " + StatAge60to + "명 입니다." ,
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
                'buttons': button_list
            },
        })


    elif stat_salary:
        return JsonResponse({
            'message': {
                'text': "stat_salary",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': button_list
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
                'text': "상품명 : " + (return_str).encode('utf-8') + "\n" +
                        "평균금리 : " + str(loanGoods.avg_int_rat) +"%\n" +
                        "최고대출금액 : " + str(loanGoods.money_credit_line) + "원\n" +
                        "상품설명 : " + (loanGoods.chatbot_description).encode('utf-8') +
                        "\n카톡 추천수 : " + str(loanGoods.chat_recommend) + "번\n" +
                        "자세히 보기 : " + str((loanGoods.loan_url).encode('utf-8')),
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
