# coding=utf-8
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from answer.models import LoanGoods, StatisticAge2, StatisticList2, StatisticLoanAmount2, StatisticSalary2, Banks, User
import json


button_list = ['시작하기', '모든 전세상품(랭킹순)', '실시간 통계보기', '우리는 하월이다', '도움말']
stat_list = ['실시간 고객 나이대별 선호은행', '실시간 고객 대출액별 선호은행', '실시간 고객 연봉', '나가기']
start_list = ['전세금액입력', '연봉입력', '대출받으실 금액입력', '계산하기', '입력정보 초기화','나가기']
LoanGoodsList = list(LoanGoods.objects.values_list('loan_good_name', flat=True))[2:5]
LoanAllList = list(LoanGoods.objects.values_list('loan_good_name', flat=True))

# 나이통계 인원 수
StatAge20to30 = str(list(StatisticAge2.objects.all())[0].m20_30)
StatAge30to40 = str(list(StatisticAge2.objects.all())[0].m30_40)
StatAge40to50 = str(list(StatisticAge2.objects.all())[0].m40_50)
StatAge50to60 = str(list(StatisticAge2.objects.all())[0].m50_60)
StatAge60to = str(list(StatisticAge2.objects.all())[0].m60_0)

# 나이통계 은행번호
StatAge20to30BankNum = list(StatisticAge2.objects.all())[1].m20_30
StatAge30to40BankNum = list(StatisticAge2.objects.all())[1].m30_40
StatAge40to50BankNum = list(StatisticAge2.objects.all())[1].m40_50
StatAge50to60BankNum = list(StatisticAge2.objects.all())[1].m50_60
StatAge60toBankNum = list(StatisticAge2.objects.all())[1].m60_0

# 나이통계 은행이름
StatAge20to30Bank = Banks.objects.get(bank_id = StatAge20to30BankNum)
StatAge30to40Bank = Banks.objects.get(bank_id = StatAge30to40BankNum)
StatAge40to50Bank = Banks.objects.get(bank_id = StatAge40to50BankNum)
StatAge50to60Bank = Banks.objects.get(bank_id = StatAge50to60BankNum)
StatAge60toBank = Banks.objects.get(bank_id = StatAge60toBankNum)

# 대출액통계 인원 수
StatLoan00to03 = str(list(StatisticLoanAmount2.objects.all())[0].m0_3)
StatLoan03to05 = str(list(StatisticLoanAmount2.objects.all())[0].m3_5)
StatLoan05to07 = str(list(StatisticLoanAmount2.objects.all())[0].m5_7)
StatLoan07to10 = str(list(StatisticLoanAmount2.objects.all())[0].m7_10)
StatLoan10to15 = str(list(StatisticLoanAmount2.objects.all())[0].m10_15)
StatLoan15to20 = str(list(StatisticLoanAmount2.objects.all())[0].m15_20)
StatLoan20to0 = str(list(StatisticLoanAmount2.objects.all())[0].m20_0)

# 대출액통계 은행번호
StatLoan00to03BankNum = list(StatisticLoanAmount2.objects.all())[1].m0_3
StatLoan03to05BankNum = list(StatisticLoanAmount2.objects.all())[1].m3_5
StatLoan05to07BankNum = list(StatisticLoanAmount2.objects.all())[1].m5_7
StatLoan07to10BankNum = list(StatisticLoanAmount2.objects.all())[1].m7_10
StatLoan10to15BankNum = list(StatisticLoanAmount2.objects.all())[1].m10_15
StatLoan15to20BankNum = list(StatisticLoanAmount2.objects.all())[1].m15_20
StatLoan20to0BankNum = list(StatisticLoanAmount2.objects.all())[1].m20_0

# 대출액통계 은행이름
StatLoan00to03Bank = Banks.objects.get(bank_id = StatLoan00to03BankNum)
StatLoan03to05Bank = Banks.objects.get(bank_id = StatLoan03to05BankNum)
StatLoan05to07Bank = Banks.objects.get(bank_id = StatLoan05to07BankNum)
StatLoan07to10Bank = Banks.objects.get(bank_id = StatLoan07to10BankNum)
StatLoan10to15Bank = Banks.objects.get(bank_id = StatLoan10to15BankNum)
StatLoan15to20Bank = Banks.objects.get(bank_id = StatLoan15to20BankNum)
StatLoan20to0Bank = Banks.objects.get(bank_id = StatLoan20to0BankNum)

# 연봉통계 인원 수
StatSalary0to2 = str(list(StatisticSalary2.objects.all())[0].m0_2)
StatSalary2to3 = str(list(StatisticSalary2.objects.all())[0].m2_3)
StatSalary3to4 = str(list(StatisticSalary2.objects.all())[0].m3_4)
StatSalary4to5 = str(list(StatisticSalary2.objects.all())[0].m4_5)
StatSalary5to7 = str(list(StatisticSalary2.objects.all())[0].m5_7)
StatSalary7to10 = str(list(StatisticSalary2.objects.all())[0].m7_10)
StatSalary10to = str(list(StatisticSalary2.objects.all())[0].m10_0)

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
    user_key = return_json_str['user_key']

    input_again = check_is_inputAgain(return_str)
    exit = check_is_exit(return_str) # exit
    rankAll = check_is_rankAll(return_str)  # ranking

    stat = check_is_stat(return_str)  # stat
    stat_age = check_is_stat_age(return_str)
    stat_loan = check_is_stat_loan(return_str)
    stat_salary = check_is_stat_salary(return_str)

    input_bank1 = check_is_input_bank1(return_str)
    input_bank2 = check_is_input_bank2(return_str)
    input_bank3 = check_is_input_bank3(return_str)
    input_bank4 = check_is_input_bank4(return_str)
    input_bank5 = check_is_input_bank5(return_str)
    input_bank6 = check_is_input_bank6(return_str)
    
    
    help = check_is_help(return_str)  # help
    goods = check_is_goods(return_str)
    test_ranking = list(LoanGoods.objects.values_list('loan_good_name', flat=True).order_by('-chat_recommend'))
    test_ranking_Str = "\n * ".join(test_ranking).encode('utf8')

    user_check = len(list(User.objects.values_list('user_key', flat=True).filter(user_key=user_key)))


    # if start button check
    print(return_str) # 리턴문 확인용
    print(user_check) # 세션확인용

    # 전체랭킹보기 버튼
    if rankAll:
        return JsonResponse({
            'message': {
                'text': "가장 인기있는 전세자금대출 상품 랭킹입니다. 현재 순위는 다음과 같습니다. \n * " + test_ranking_Str,
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': test_ranking # DB에 넣어서 list로 출력
            },
        })

    # 도움말 버튼
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

    # 나가기 버튼
    elif exit:
        return JsonResponse({
            'message': {
                'text': "초기화면으로 돌아갑니다.",

            },
            'keyboard': {
                'type': 'buttons',
                'buttons': button_list
            },
        })

    # 메인화면 통계
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

    # 이용고객 나이통계 및 나이별 선호은행
    elif stat_age:
        return JsonResponse({
            'message': {
                'text': "* 현재 하월의 이용고객은 \n20대 ~ 30대 : " + StatAge20to30 + "명 \n" +
                        "30대 ~ 40대 : " + StatAge30to40 + "명\n40대 ~ 50대 : " + StatAge40to50 + "명 \n" +
                        "50대 ~ 60대 : " + StatAge50to60 + "명\n60대 이상 : " + StatAge60to + "명 입니다." +
                        "\n\n* 연령대별 선호은행은 \n20대 ~ 30대 : " + (StatAge20to30Bank.bank_name).encode('utf-8') + "\n" +
                        "30대 ~ 40대 : " + (StatAge30to40Bank.bank_name).encode('utf-8') +
                        "\n40대 ~ 50대 : " + (StatAge40to50Bank.bank_name).encode('utf-8') +
                        "\n50대 ~ 60대 : " + (StatAge50to60Bank.bank_name).encode('utf-8') +
                        "\n60대 이상 : " + (StatAge60toBank.bank_name).encode('utf-8') + " 입니다.",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': stat_list
            },
        })


    # 이용고객 대출액 통계 및 대출액별 선호은행
    elif stat_loan:
        return JsonResponse({
            'message': {
                'text': "* 현재 하월의 대출액별 분류는 \n2천만원 이하 : " + StatLoan00to03  + "명\n" +
                        "2천만원 ~ 3천만원 : " + StatLoan03to05  + "명\n5천만원 ~ 7천만원 : " + StatLoan05to07  + "명\n" +
                        "7천만원 ~ 1억원 : " + StatLoan07to10  + "명\n1억원 ~ 1억5천만원 : " + StatLoan10to15  + "명\n" +
                        "1억 5천만원 ~ 2억원 : " + StatLoan15to20  + "명\n2억원 이상 : " + StatLoan20to0  + "명 입니다." +
                        "\n\n* 대출액별 선호은행은 \n3천만원 이하 : " + (StatLoan00to03Bank .bank_name).encode('utf-8') +
                        "\n3천만원 ~ 5천만원 : " + (StatLoan03to05Bank.bank_name).encode('utf-8') +
                        "\n5천만원 ~ 7천만원 : " + (StatLoan05to07Bank.bank_name).encode('utf-8') +
                        "\n7천만원 ~ 1억원 : " + (StatLoan07to10Bank.bank_name).encode('utf-8') +
                        "\n1억원 ~ 1억5천만원 : " + (StatLoan10to15Bank.bank_name).encode('utf-8') +
                        "\n1억원 5천만원 ~ 2억원 : " + (StatLoan15to20Bank.bank_name).encode('utf-8') +
                        "\n2억원 이상 : " + (StatLoan20to0Bank.bank_name).encode('utf-8') + " 입니다.",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': stat_list
            },
        })


    # 이용고객 연봉 통계
    elif stat_salary:
        return JsonResponse({
            'message': {
                'text': "* 현재 하월고객의 연봉은 \n2천만원 이하 : " + StatSalary0to2 + "명\n" +
                        "2천만원 ~ 3천만원 : " + StatSalary2to3 + "명\n3천만원 ~ 4천만원 : " + StatSalary3to4 + "명\n" +
                        "4천만원 ~ 5천만원 : " + StatSalary4to5 + "명\n5천만원 ~ 7천만원 : " + StatSalary5to7 + "명\n" +
                        "7천만원 ~ 1억원 : " + StatSalary7to10 + "명\n1억원 이상 : " + StatSalary10to + "명입니다.",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': stat_list
            },
        })

    # 상품 상세보기 및 추천
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

    # 다시시작
    elif input_again:
        user = User.getUser(user_key=user_key)
        user.delete()

        return JsonResponse({
            'message': {
                'text': "다시시작합니다.",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': button_list
            },
        })

    # 하나은행
    elif input_bank1:
        # User.setUserInputLending(user_key, return_str)
        User.setUserInputBank(user_key, 1)
        user = User.getUser(user_key=user_key)
        result_lending = user.input_lending
        result_salary = user.input_salary
        result_loan = user.input_loan
        result_bank1 = list(LoanGoods.objects.values_list('loan_good_name', flat=True).filter(loan_bank_id=1))

        print("하나은행 실행됨")
        return JsonResponse({
            'message': {
                'text': "고객님께서 입력하신 값은 \n전세금 : " + str(result_lending) + "\n연봉 : " + str(result_salary) + "\n대출금 : " +
                        str(result_loan) + "\n은행 : 하나은행 입니다. \n\n고객님께서 대출 받으실 수 있는 최고 한도는 " +
                        str(max(result_lending * 0.8, result_salary * 3.5)) + "(연봉 * 3.5와 전세금의 80%중 높은값)입니다." +
                "\n하월은 위와같은 조건에서 아래의 상품을 추천합니다. (같은 조건의 상품중 최저금리 상품)",
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': [result_bank1]
            },
        })

    else:
        # loanGoods = LoanGoods.objects.get(loan_good_name=(return_str).encode('utf-8'))
        if user_check == 0:
            User.createUser(user_key)
            return JsonResponse({
                'message': {
                    'text': "사회초년생에게 맞는 전세자금대출 추천을 시작합니다. \n저희 서비스를 이용하기 위해서는\n" +
                    "총 4가지 정보가 필요합니다. \n고객님께서 들어가실 집의 전세금액, 연봉, 대출금액, 그리고 주거래 은행 이 필요합니다.\n" +
                    "우선 고객님이 들어가실 집의 전세금액을 입력해 주세요. \nex) 9000",
                },
                'keyboard': {
                    'type': 'text'
                },
            })

        elif User.getUser(user_key=user_key).input_lending == 0:
            User.setUserInputLending(user_key, (return_str).encode('utf-8'))

            print("input_lending 실행됨")
            return JsonResponse({
                'message': {
                    'text': "고객님이 들어가실 집의 전세금액으로" + (return_str).encode('utf-8') +"원을 입력받았습니다. 고객님의 연봉을 입력하여 주세요.\n" +
                            "주의 - 만원은 생략됩니다.\nex) 2400\n\n입력창에 다시 라고 입력하시면 다시입력하실 수 있습니다.",
                },
                'keyboard': {
                    'type': 'text'
                },
            })

        elif User.getUser(user_key=user_key).input_lending > 0 and User.getUser(user_key=user_key).input_salary == 0:
            User.setUserInputSalary(user_key, (return_str).encode('utf-8'))

            print("input_salary 실행됨")
            return JsonResponse({
                'message': {
                    'text': "고객님의 연봉으로" + (return_str).encode('utf-8') + "원을 입력받았습니다. 고객님께서 필요하신" +
                            " 대출금액을 입력하여 주세요.\n" +
                            "주의 - 만원은 생략됩니다.\nex) 7000\n\n입력창에 다시 라고 입력하시면 다시입력하실 수 있습니다.",
                },
                'keyboard': {
                    'type': 'text'
                },
            })

        elif User.getUser(user_key=user_key).input_salary > 0 and User.getUser(user_key=user_key).input_loan == 0:
            User.setUserInputLoan(user_key, (return_str).encode('utf-8'))

            print("input_loan 실행됨")
            return JsonResponse({
                'message': {
                    'text': "고객님의 대출금으로" + (return_str).encode('utf-8') + "원을 입력받았습니다. \n마지막 입니다!" +
                            "주 거래은행을 선택하여 주세요",
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': ['하나은행', '신한은행', '우리은행', '국민은행', '농협', '기업은행']
                },
            })

        else:
            # elif input_lending:
            print("else문 실행 오류확인")
            user = User.getUser(user_key=user_key)
            user.delete()
            return JsonResponse({
                'message': {
                    'text': "잘못입력하셨습니다"
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': button_list
                },
            })


# user input is start button check
def check_is_start(str):
    if str == ("시작하기").decode('utf-8'):
        return True
    else:
        return False


def check_is_inputAgain(str):
    if str == ("다시").decode('utf-8') or str == ("처음").decode('utf-8') or str == ("처음으로").decode('utf-8'):
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

def check_is_exit(str):
    if str == ("나가기").decode('utf-8'):
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
    if str == ("실시간 고객 나이대별 선호은행").decode('utf-8'):
        return True
    else:
        return False


def check_is_stat_loan(str):
    if str == ("실시간 고객 대출액별 선호은행").decode('utf-8'):
        return True
    else:
        return False


def check_is_stat_salary(str):
    if str == ("실시간 고객 연봉").decode('utf-8'):
        return True
    else:
        return False


def check_is_input_lending(str):
    if str == ("전세금액입력").decode('utf-8'):
        return True
    else:
        return False


def check_is_input_salary(str):
    if str == ("연봉입력").decode('utf-8'):
        return True
    else:
        return False


def check_is_input_loan(str):
    if str == ("대출받으실 금액입력").decode('utf-8'):
        return True
    else:
        return False


def check_is_input_bank1(str):
    if str == ("하나은행").decode('utf-8'):
        return True
    else:
        return False


def check_is_input_bank2(str):
    if str == ("신한은행").decode('utf-8'):
        return True
    else:
        return False
    
    
def check_is_input_bank3(str):
    if str == ("우리은행").decode('utf-8'):
        return True
    else:
        return False


def check_is_input_bank4(str):
    if str == ("국민은행").decode('utf-8'):
        return True
    else:
        return False
    
    
def check_is_input_bank5(str):
    if str == ("농협").decode('utf-8'):
        return True
    else:
        return False


def check_is_input_bank6(str):
    if str == ("기업은행").decode('utf-8'):
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
