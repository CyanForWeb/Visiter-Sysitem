from django.shortcuts import render
from django.utils import timezone
from .models import Post


def home(request):
    return render(request, 'html_Guest/Guest_home.html', )


#その他　客人の画面で使用する機能たち
def other(request):
    return render(request, 'html_Guest/Guest_other.html', )

def other_form1(request):
    return render(request, 'html_Guest/Guest_other_form1.html', )

def other_form2(request):
    return render(request, 'html_Guest/Guest_other_form2.html', )

def other_form3(request):
    return render(request, 'html_Guest/Guest_other_form3.html', )

def other_form4(request):
    return render(request, 'html_Guest/Guest_other_form4.html', )

def other_end(request):
    return render(request, 'html_Guest/Guest_other_end.html', )


#配達員　の画面で使用する機能たち
def delivery(request):
    return render(request, 'html_Guest/Guest_delivery.html', )

def delivery_stamp(request):
    return render(request, 'html_Guest/Guest_delivery_stamp.html', )

def delivery_end1(request):
    return render(request, 'html_Guest/Guest_delivery_end1.html', )


#ポスト投函　の画面で使用する機能たち
def post(request):
    return render(request, 'html_Guest/Guest_post.html', )

def post_end1(request):
    return render(request, 'html_Guest/Guest_post_end1.html', )

def post_pic(request):
    return render(request, 'html_Guest/Guest_post_pic.html', )

def post_end2(request):
    return render(request, 'html_Guest/Guest_post_end2.html', )
