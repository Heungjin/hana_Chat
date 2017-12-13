# coding=utf-8
from django.contrib import admin
from .models import LoanGoods # 모델에서 LoanGoods를 불러온다
from .models import CustomerInfo # 모델에서 CustomerInfo를 불러온다
from .models import Banks # 모델에서 Banks를 불러온다
# from .models import StatisticAge # 모델에서 StatisticAge를 불러온다
# from .models import StatisticList # 모델에서 StatisticAge를 불러온다


# 출력할 테이블
# 고객정보테이블
class CustomerInfoAdmin(admin.ModelAdmin):
  list_display = ('cus_num', 'cus_age', 'cus_sex', 'repayment','repayment_money','cus_salary','cus_loan','leasing_mortgage','month_loan_period', 'bank_id', 'input_date')

# 상품정보테이블
class LoanGoodsAdmin(admin.ModelAdmin):
  list_display = ('loan_good_num', 'loan_good_name', 'loan_bank', 'avg_int_rat','money_credit_line','rate_credit_line','salary_credit_line','month_loan_period_line','loan_repayment', 'loan_url', 'loan_img','num_recommend','chatbot_img','chatbot_description','chat_recommend')

# 은행정보테이블
class BanksAdmin(admin.ModelAdmin):
  list_display = ('bank_id', 'bank_name', 'bank_image')

# 나이대별 통계테이블
# class StatisticAgeAdmin(admin.ModelAdmin):
#   list_display = ('type', 'm0_20', 'm20_30', 'm30_40', 'm40_50', 'm50_60', 'm60_0')
#
#
# # 웹에서 가장 많이 추천된 상품
# class StatisticListAdmin(admin.ModelAdmin):
#   list_display = ('type', 'm1_loan_good_num', 'm1_num', 'm2_loan_good_num', 'm2_num', 'm3_loan_good_num', 'm3_num', 'total')


# 클래스를 어드민 사이트에 등록한다.
admin.site.register(CustomerInfo, CustomerInfoAdmin)
admin.site.register(LoanGoods, LoanGoodsAdmin)
admin.site.register(Banks, BanksAdmin)
# admin.site.register(StatisticAge, StatisticAgeAdmin)
# admin.site.register(StatisticList, StatisticListAdmin)