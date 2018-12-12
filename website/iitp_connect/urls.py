from . import views
from django.conf.urls import url
from django.urls import path

app_name='iitp_connect'

urlpatterns = [
    url(r'^$',views.index,name='index'),

    url(r'^register/$',views.UserFormView.as_view(), name='register'),

    url(r'^login_user/$', views.login_user, name='login_user'),

    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    url(r'^login_user/detail/$', views.detail, name='detail'),

    url(r'^about/$', views.about, name='about'),

    url(r'^login_user/detail/item/$', views.create_item, name='create_item'),

    url(r'^login_user/item/(?P<item_id>[0-9]+)/update/status/$', views.update_status, name='update_status'),

    url(r'^login_user/detail/item/(?P<item_id>[0-9]+)/view', views.item_view, name='item_view'),

    url(r'^login_user/detail/item/(?P<item_id>[0-9]+)/edit', views.item_edit, name='item_edit'),

    url(r'^lost_found/detail', views.lost_found, name='lost_found'),

    url(r'^buy_sell/detail', views.buy_sell, name='buy_sell'),

    url(r'^item_gen/(?P<item_id>[0-9]+)/$', views.item_general, name='item_general'),

    url(r'^item/(?P<item_id>[0-9]+)/claim/$', views.claim, name='claim'),

    url(r'^login_user/detail/cab_service/$', views.cab_service, name='cab_service'),

    url(r'^login_user/detail/booking/$', views.booking, name='booking'),

    url(r'^login_user/detail/booking/(?P<book_id>[0-9]+)/edit/$', views.booking_edit, name='booking_edit'),

    url(r'^login_user/booking/(?P<book_id>[0-9]+)/update/status/$', views.update_book_status, name='update_book_status'),

    url(r'^cab/(?P<book_id>[0-9]+)/claim/$', views.claim_book, name='claim_book'),

    path('cab_share/<int:p_year>/<int:p_month>/$', views.cab_share, name='cab_share'),

    path('cab_book/<int:p_year>/<int:p_month>/<int:p_day>/$', views.cab_book, name='cab_book'),

    # path('login_user/detail/upload', views.upload, name='upload'),

    # url(r'^cab_share/$', views.home, name='home'),

    # url(r'^login_user/profile/(?P<document_id>[0-9]+)/$', views.profile_status, name='profile_status'),
]

