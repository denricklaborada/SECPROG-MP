from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone


class UsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        self.check_users()

        admin = User.objects.get(username="admin")
        admin.usertypes = "Administrator"

        admin.save()

        response = self.get_response(request)

        return response

    def check_users(self):
        product_managers = User.objects.filter(usertypes="ProductManager")
        accounting_managers = User.objects.filter(usertypes="AccountingManager")

        for product_manager in product_managers:
            if product_manager.temporary and (timezone.now() - product_manager.date_joined) > timedelta(1):
                product_manager.expired = True
                product_manager.save()

        for accounting_manager in accounting_managers:
            if accounting_manager.temporary and (timezone.now() - accounting_manager.date_joined) > timedelta(1):
                accounting_manager.expired = True
                accounting_manager.save()
