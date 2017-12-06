# coding=utf-8
from django.contrib import admin
from .models import LoanGoods # 모델에서 LoanGoods를 불러온다
from .models import CustomerInfo # 모델에서 CustomerInfo를 불러온다


# 출력할 테이블
class CustomerInfoAdmin(admin.ModelAdmin):
  list_display = ('cus_num', 'cus_age', 'cus_sex', 'repayment','repayment_money','cus_salary','cus_loan','leasing_mortgage','month_loan_period', 'bank_id', 'input_date')


class LoanGoodsAdmin(admin.ModelAdmin):
  list_display = ('loan_num', 'loan_good_name', 'loan_bank', 'avg_int_rat','money_credit_line','rate_credit_line','salary_credit_line','month_loan_period_line','loan_repayment', 'loan_url', 'loan_img','num_recommend')

# 클래스를 어드민 사이트에 등록한다.
admin.site.register(CustomerInfo, CustomerInfoAdmin)
admin.site.register(LoanGoods, LoanGoodsAdmin)