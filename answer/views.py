# coding=utf-8
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from answer.models import LoanGoods
# from bs4 import BeautifulSoup
# from urllib.request import urlopen
import json

button_list = ['시작하기', '모든 전세상품(랭킹순)', '인천지역 주택분양정보', '실시간 통계보기', '내기', '도움말']
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
    # rental = crawl(return_str)  # crawl
    gamble = check_is_gamble(return_str)  # gamble
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

    # elif rental:
    #     return JsonResponse({
    #         'message': {
    #             'text': "인천지역의 공공임대주택을 포함한 인천지역의 주택분양정보를 크롤링하여 출력합니다.",
    #         },
    #         'keyboard': {
    #             'type': 'buttons',
    #             'buttons': ['나가기']
    #         },
    #     })

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

######################################### 크롤링 ######################################
# def crawl(request):
#     # 메뉴 DB 테이블 비우기
#     flush_menu_db()
#
#     # 메뉴 테이블 추출
#     html = urlopen('http://dgucoop.dongguk.edu/store/store.php?w=4&l=1')
#     source = html.read().decode('cp949', 'ignore')
#     html.close()
#     soup = BeautifulSoup(source, "html.parser", from_encoding='utf-8')
#     table_div = soup.find(id="sdetail")
#     menu_tables = table_div.table.tr.td.p.find_all('table', {"bgcolor": "#CDD6B5"})
#
#     #식당별 테이블 지정
#     kyo_table = menu_tables[0]
#
#     # 교직원 식당
#     if kyo_table.find(text="휴무"):
#         create_menu_db_table('집밥', '중식', '휴무 \n')
#         create_menu_db_table('한그릇', '중식', '휴무 \n')
#         create_menu_db_table('집밥', '석식', '휴무 \n')
#         create_menu_db_table('한그릇', '석식', '휴무 \n')
#
#     else:
#         # 중식이 검색이 안되는 문제 발생... 일단 원래 방법으로 구현해놓음
#         kyo_trs = kyo_table.find_all('tr')
#         kyo_tables = kyo_trs[1].find_all('table')
#
#         kyo_jib_trs = kyo_tables[0].find_all('tr')
#         kyo_jib_menu = kyo_jib_trs[0].text
#         kyo_jib_price = kyo_jib_trs[1].text
#
#         kyo_han_trs = kyo_tables[1].find_all('tr')
#         kyo_han_menu = kyo_han_trs[0].text
#         kyo_han_price = kyo_han_trs[1].text
#
#         create_menu_db_table('집밥', '중식', kyo_jib_menu + kyo_jib_price)
#         create_menu_db_table('한그릇', '중식', kyo_han_menu + kyo_han_price)
#
#         for tr in kyo_trs:
#             if tr.find(text='석식'):
#                 kyo_tables = tr.find_all('table')
#
#                 kyo_jib_trs = kyo_tables[0].find_all('tr')
#                 kyo_jib_menu = kyo_jib_trs[0].text
#                 kyo_jib_price = kyo_jib_trs[1].text
#
#                 create_menu_db_table('집밥', '석식', kyo_jib_menu + kyo_jib_price)
#
#         return JsonResponse({
#             'message': {
#                 'text': "크롤링 실행",
#             },
#             'keyboard': {
#                 'type': 'buttons',
#                 'buttons': menu_tables # start button for user
#             },
#         })

    ##################################################################################
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

# def check_is_rental(str):
#     if str == ("인천지역 주택분양정보").decode('utf-8'):
#         return True
#     else:
#         return False


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
