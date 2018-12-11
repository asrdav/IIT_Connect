from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import *
from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.mail import send_mail
from calendar import monthrange
from datetime import datetime

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def index(request):
    current_month = datetime.now().month
    current_year = datetime.now().year
    return render(request, 'iitp_connect/index.html', {'curr_y': current_year, 'curr_m': current_month})


def lost_found(request):
    items = Item.objects.all()
    # items = Item.objects.none()
    if items:
        return render(request, 'iitp_connect/lost_found.html', {'items': reversed(items)})
        # for user_act in users:
        #     items_res = Item.objects.filter(user=user_act)
        #     items = items | items_res
    else:
        return redirect('iitp_connect:index')


def item_general(request, item_id):
    item = Item.objects.get(pk=item_id)
    return render(request, 'iitp_connect/view.html', {'item': item})


def buy_sell(request):
    items = Item.objects.all()
    # items = Item.objects.none()
    if items:
        return render(request, 'iitp_connect/buy_sell.html', {'items': reversed(items)})
        # for user_act in users:
        #     items_res = Item.objects.filter(user=user_act)
        #     items = items | items_res
    else:
        return redirect('iitp_connect:index')


def detail(request):
    if not request.user.is_authenticated:
        return render(request, 'iitp_connect/login.html')
    else:
        items = Item.objects.filter(user=request.user)
        document = Document.objects.filter(user=request.user)

        query = request.GET.get("q")
        if query:
            items = items.filter(
                Q(item_name__icontains=query) |
                Q(item_tag__icontains=query)
            ).distinct()
            return render(request, 'iitp_connect/detail.html', {
                'items': items,
                'document': document
            })
        else:
            return render(request, 'iitp_connect/detail.html', {'items': reversed(items), 'document': document})



# def profile_status(request, document_id):
#     if not request.user.is_authenticated:
#         return render(request, 'iitp_connect/login.html')
#     else:
#         document = Document.objects.get(pk=document_id)
#
#         document.profile_pic = "/media/{request.user.username}/{filename}"
#         document.save()
#
#         return redirect('iitp_connect:detail')


def item_view(request, item_id):
    if not request.user.is_authenticated:
        return render(request, 'iitp_connect/login.html')
    else:
        item = Item.objects.get(pk=item_id)
        return render(request, 'iitp_connect/view.html', {'item': item})


def item_edit(request, item_id):
    if not request.user.is_authenticated:
        return render(request, 'iitp_connect/login.html')
    else:
        form = ItemForm(request.POST or None, request.FILES or None, instance=Item.objects.get(pk=item_id))
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user

            # item.item_logo = request.FILES['item_logo']
            #
            # file_type = item.item_logo.url.split('.')[-1]
            # file_type = file_type.lower()
            # if file_type not in IMAGE_FILE_TYPES:
            #     context = {
            #         'form': form,
            #         'error_message': 'Image file must be PNG, JPG, or JPEG',
            #     }
            #     return render(request, 'iitp_connect/create_item.html', context)

            item.save()

            '''items = Item.objects.filter(user=request.user)
            query = request.GET.get("q")   
            if query:
                items = items.filter(
                    Q(item_name=query)
                ).distinct()
                return render(request, 'iitp_connect/detail.html', {
                    'items': items,
                })
            else:   '''

            return redirect('iitp_connect:detail')
        context = {
            'form': form,
        }
        return render(request, 'iitp_connect/edit_item.html', context)


def update_status(request, item_id):
    if not request.user.is_authenticated:
        return render(request, 'iitp_connect/login.html')
    else:
        item = Item.objects.get(pk=item_id)

        if item.item_status == 'Open':
            item.item_status = 'Closed'
        else:
            item.item_status = 'Open'
        item.save()
        return redirect('iitp_connect:detail')


# def model_form_upload(request):
#
#     # if request.method == 'POST':
#
#     form = DocumentForm(request.POST, request.FILES)
#     if form.is_valid():
#         form.user = request.user
#         form.save()
#         return redirect('iitp_connect:detail')

    # ''' else:
    #     form = DocumentForm()
    # return render(request, 'iitp_connect/model_form_upload.html', {
    #     'form': form
    # })  '''

# def lost_found(request):

# def buy_sell(request):

# def create_item_view(request, item_id):

# def create_item_edit(request, item_id):


def about(request):
    return render(request, 'iitp_connect/about.html')


def claim(request, item_id):
    if not request.user.is_authenticated:
        return redirect('iitp_connect:login_user')
    else:
        item = Item.objects.get(pk=item_id)
        user_ids = Item.objects.filter(pk=item_id).values_list('user', flat=True)
        users = User.objects.get(id__in=user_ids)
        send_mail(
            'Regarding the online inventory portal',
            'If your item has been lost/found or '
            'want to buy/sell and you have registered it in the '
            'online inventory, then contact the person with the mail_id:  ' + request.user.email + '\n' + 'The '
            'item name is:  ' + item.item_name + '\nThe item description is:  ' + item.item_description,

            request.user.email,
            [users.email],
            fail_silently=False,
        )
        # print(request.user.email)
        # print(users.email)
        return redirect('iitp_connect:index')


def create_item(request):
    if not request.user.is_authenticated:
        return redirect('iitp_connect:login_user')
    else:
        form = ItemForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.item_pic = request.FILES['item_pic']
            file_type = item.item_pic.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'iitp_connect/create_item.html', context)
            item.save()

            '''items = Item.objects.filter(user=request.user)
            query = request.GET.get("q")   
            if query:
                items = items.filter(
                    Q(item_name=query)
                ).distinct()
                return render(request, 'iitp_connect/detail.html', {
                    'items': items,
                })
            else:   '''

            return redirect('iitp_connect:detail')
        context = {
            'form': form,
        }
        return render(request, 'iitp_connect/create_item.html', context)


class UserFormView(View):
    form_class = UserForm
    template_name = 'iitp_connect/registration_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('iitp_connect:login_user')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('iitp_connect:login_user')
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('iitp_connect:login_user')

        return render(request, self.template_name, {'form': form})


def logout_user(request):
    logout(request)
    return redirect('iitp_connect:login_user')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('iitp_connect:detail')

        # items = Item.objects.filter(user=request.user)
        # return render(request, 'iitp_connect/detail.html', {'items': items})

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('iitp_connect:detail')

                # items = Item.objects.filter(user=request.user)
                # return render(request, 'iitp_connect/detail.html', {'items': items})

            else:
                return render(request, 'iitp_connect/login.html', {'error_message': 'Your account has been disabled.'})
        else:
            return render(request, 'iitp_connect/login.html', {'error_message': 'Invalid login.'})
    return render(request, 'iitp_connect/login.html')


def named_month(p_month_number):
    """
    Return the name of the month, given the month number
    """
    return date(1900, p_month_number, 1).strftime('%B')

#
# def home(request):
#     """
#     Show calendar of events this month
#     """
#     l_today = datetime.now()
#     return cab_share(request, l_today.year, l_today.month)


def cab_share(request, p_year, p_month):
    """
    Show calendar of events for specified month and year
    """
    l_year = int(p_year)
    l_month = int(p_month)
    # l_calendar_from_month = datetime(l_year, l_month, 1)
    # l_calendar_to_month = datetime(l_year, l_month, monthrange(l_year, l_month)[1])

    cab_shares = CabService.objects.order_by('date_time').filter(book_status="Booked", date_time__year=p_year,
                                                                 date_time__month=p_month)

    # lContestEvents=ContestEvent.objects.filter(date_of_event__gte=lCalendarFromMonth, date_of_event__
    # lte=lCalendarToMonth)

    l_calendar = CabshareCalendar(cab_shares).formatmonth(l_year, l_month)
    l_previous_year = l_year
    l_previous_month = l_month - 1

    if l_previous_month == 0:
        l_previous_month = 12
        l_previous_year = l_year - 1
    l_next_year = l_year
    l_next_month = l_month + 1
    if l_next_month == 13:
        l_next_month = 1
        l_next_year = l_year + 1
    l_year_after_this = l_year + 1
    l_year_before_this = l_year - 1

    last_day = monthrange(l_year, l_month)[1]
    return render(request, 'iitp_connect/calendar.html', {'Calendar': mark_safe(l_calendar), 'Month': l_month,
                                                          'MonthName': named_month(l_month), 'Year': l_year,
                                                          'PreviousMonth': l_previous_month,
                                                          'PreviousMonthName': named_month(l_previous_month),
                                                          'PreviousYear': l_previous_year,
                                                          'NextMonth': l_next_month,
                                                          'NextMonthName': named_month(l_next_month),
                                                          'NextYear': l_next_year,
                                                          'YearBeforeThis': l_year_before_this,
                                                          'YearAfterThis': l_year_after_this, 'StartDay': 1,
                                                          'LastDay': last_day})


def cab_service(request):
    if not request.user.is_authenticated:
        return redirect('iitp_connect:login_user')
    else:
        form = CabServiceForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()

            return redirect('iitp_connect:detail')
        context = {
            'form': form,
        }
        return render(request, 'iitp_connect/cab_service.html', context)


def booking(request):
    if not request.user.is_authenticated:
        return redirect('iitp_connect:login_user')
    else:
        bookings = CabService.objects.filter(user=request.user)
        return render(request, 'iitp_connect/booking.html', {'bookings': reversed(bookings)})

        # query = request.GET.get("q")
        # if query:
        #     bookings = bookings.filter(
        #         Q(item_name__icontains=query) |
        #         Q(item_tag__icontains=query)
        #     ).distinct()
        #     return render(request, 'iitp_connect/booking.html', {
        #         'bookings': bookings,
        #     })
        # else:


def booking_edit(request, book_id):
    if not request.user.is_authenticated:
        return render(request, 'iitp_connect/login.html')
    else:
        form = CabServiceForm(request.POST or None, request.FILES or None, instance=CabService.objects.get(pk=book_id))
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user

            book.save()

            return redirect('iitp_connect:booking')
        context = {
            'form': form,
        }
        return render(request, 'iitp_connect/edit_booking.html', context)


def update_book_status(request, book_id):
    if not request.user.is_authenticated:
        return render(request, 'iitp_connect/login.html')
    else:
        book = CabService.objects.get(pk=book_id)

        if book.book_status == 'Booked':
            book.book_status = 'Unbooked'
        else:
            book.book_status = 'Booked'
        book.save()
        return redirect('iitp_connect:booking')


def cab_book(request, p_year, p_month, p_day):
    if not request.user.is_authenticated:
        return render(request, 'iitp_connect/login.html')
    else:
        user = User.objects.all()
        cab_sr = CabService.objects.filter(~Q(user=request.user))
        return render(request, 'iitp_connect/cab_book.html', {'bookings': cab_sr, 'p_year': p_year, 'p_month': p_month,
                                                              'p_day': p_day})


def claim_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect('iitp_connect:login_user')
    else:
        user_ids = CabService.objects.filter(pk=book_id).values_list('user', flat=True)
        users = User.objects.get(id__in=user_ids)
        send_mail(
            'Regarding the online CabShare request',
            'If you have posted a request for sharing cab'
            ' in online portal , someone with  mail_id:  ' + request.user.email + '\n' + 'wants to share cab with you.',

            request.user.email,
            [users.email],
            fail_silently=False,
        )
        # print(request.user.email)
        # print(users.email)
        return redirect('iitp_connect:index')

#
# def upload(request):
#     if not request.user.is_authenticated:
#         return redirect('iitp_connect:login_user')
#     else:
#         return redirect('iitp_connect:index')
