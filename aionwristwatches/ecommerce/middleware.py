from ecommerce.models import ProductManager, AccountingManager

class UsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):

        print("puta")
        self.check_users()
        response = self.get_response(request)

        return response

    def check_users(self):
        product_managers = ProductManager.objects.all()
        accounting_managers = AccountingManager.objects.all()

        for product_manager in product_managers:
            if product_manager.is_expired():
                print(product_manager.datecreated)
                product_manager.delete()
    
        for accounting_manager in accounting_managers:
            if accounting_manager.is_expired():
                print(accounting_manager.datecreated)
                accounting_manager.delete()