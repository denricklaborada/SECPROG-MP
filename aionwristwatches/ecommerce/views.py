import re, json, logging

from django.contrib.auth.models import User
from django.contrib.auth.views import login, logout
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from .forms import RegistrationForm, ReviewForm
from .models import Product, Transaction, Review

logger = logging.getLogger(__name__)

def outlog(request):
    try:
        uname = request.user.username
        logger.info(str(request) + '  User:' + uname + " logged out!")
    except:
        logger.info(str(request) + '  User: logged out!')
    return logout(request, next_page='/')

def error_400(request):
    try:
        logger.error(str(request) + ' 400 Bad request ' + request.user.username + " " + request.user.usertypes)
    except:
        logger.error(str(request) + " 400 Bad request guest")
    return render(request, 'ecommerce/400.html')

def error_403(request):
    try:
        logger.error(str(request)+ ' 403 Forbidden error '+ request.user.username + " " + request.user.usertypes)
    except:
        logger.error(str(request) + " 403 Forbidden error guest")


    return render(request, 'ecommerce/403.html')

def error_404(request):
    logger.error(str(request)+ ' 404 Page not found ' + request.user.username)
    try:
        logger.error(str(request) + ' 404 Page not found ' + request.user.username + " " + request.user.usertypes)
    except:
        logger.error(str(request) + ' 404 Page not found guest')
    return render(request,'ecommerce/404.html')
    
def error_500(request):
    try:
        logger.error(str(request) + ' 500 Internal Server Error ' + request.user.username)
    except:
        logger.error(str(request) + " 500 Internal Server Error guest")
    return render(request,'ecommerce/500.html')
    
def index(request):
    product_list = Product.objects.all()

    search = request.GET.get('search')
    searched = False
    
    erroruser = False
    error_similar = False
    error_pblack = False
    error_length = False
    error_alpha = False
    error_match = False
    error_exists = False
    
    BLACKLIST_PASSWORD = ['password', 'pass123', 'password123', 'admin', 'guest','123456','qwerty','12345678','qwertyuiop','google','zxcvbnm','111111','1234567890','123123','mynoob','18atcskd2w','1q2w3e4r','654321','letmein','football','iloveyou','welcome','monkey','abc123','passw0rd','dragon','starwars','123456789']
    BLACKLIST_USERNAME = [ 'admin', 'administrator', 'root', 'system', 'guest','operator','super','gg','test1','testing','user','111111','123456','12345678','abc123','abramov','account','accounting','ad','adm','adver','advert','advertising','afanasev','agafonov','agata','Baseball','business','company','contact','contactus','design','director','dragon','manager','marketing','mysql','oracle','password','postmaster','qwerty','test','user','webmaster']

    if search:
        product_list = product_list.filter(prodname__icontains=search).distinct()
        searched = True
        if request.user.is_authenticated:
            logger.info("User: " + request.user.username + " searched for" + search)
        else:
            logger.info("User: guest searched for" + search)
    if request.method == 'POST':
        regform = RegistrationForm(request.POST)
        print("REQUEST POST")
        
        if regform.is_valid():
            password=regform.cleaned_data['password1']
            print("FORM VALID")
            regform.save()
            regform.save()
            return redirect('/')
        
        try:
            fname_passed =  regform.cleaned_data.get('first_name')
            lname_passed =  regform.cleaned_data.get('last_name')
            username_passed = request.POST['username']
            password_passed = regform.cleaned_data.get('password1')
            password2_passed = request.POST['password2']
        except:
            pass
        
        regform = RegistrationForm()
        context = {
            'product_list': product_list,
            'regform': regform,
            'searched': searched,
            'query': search,
        }
        try:
            uname = request.POST['username']
        except:
            pass

        
        login(request, context)
        if request.user.is_authenticated:
            if request.user.usertypes == 'Customer':
                logger.info(str(request) + '  User:' + request.user.username + " login successfully !")
            else:
                logger.warning(str(request) + '  User:' + uname + " login failed !")
                logout(request)
                erroruser = True

            return login(request, context)
        elif username_passed and password_passed and fname_passed and lname_passed:
            
            # ALPHANUMERIC
            if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password_passed):
                error_alpha = True
                
            # PASSWORD IS BLACKLISTED
            elif password_passed.lower() in BLACKLIST_PASSWORD:
                error_pblack = True            
                
            elif username_passed.lower() in BLACKLIST_USERNAME:
                error_pblack = True
                
            # MIN_LENGTH IS 8
            elif len(password_passed) < 8:
                error_length = True
            
            # MATCH?
            elif password_passed != password2_passed:
                error_match = True

            # EXISTING USERNAME
            elif len(User.objects.filter(username=username_passed)) > 0:
                error_exists = True
            
            # USERNAME, FNAME, LNAME != PASSWORD
            elif username_passed.lower() in password_passed.lower():
                error_similar = True

            elif fname_passed.lower() in password_passed.lower():
                error_similar = True

            elif lname_passed.lower() in password_passed.lower():
                error_similar = True

        else:
            logger.warning(str(request) + '  User:' + uname + " login failed !")
            erroruser = True
    regform = RegistrationForm()
    context = {
        'error_length': error_length,
        'error_alpha': error_alpha,
        'error_pblack': error_pblack,
        'error_similar': error_similar,
        'error_exists': error_exists,
        'error_match': error_match,
        'erroruser': erroruser,
        'product_list': product_list,
        'regform': regform,
        'searched': json.dumps(searched),
        'query': search,
    }
    return render(request, 'ecommerce/index.html', context)

def myorders(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes != "Customer":
        return error_403(request)

    if request.user.is_authenticated:
        trans = Transaction.objects.filter(user=request.user)
        logger.info("User: " + request.user.username + " viewed personal orders")
        return render(request, 'ecommerce/myorders.html', {'trans': trans, })

    return redirect('/')


def acctman(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes != "AccountingManager":
       return error_403(request)

    product_list = Product.objects.all()
    logger.info("Accounting Manager: " + request.user.username + " viewed transactions")
    context = {
        'product_list': product_list,
    }
    return render(request, 'ecommerce/acctman.html', context)


def checkout(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated and request.user.usertypes=="Customer" and request.method == "POST":
        user = request.user
        qty = request.POST['quantity']
        total = request.POST['total']

        trans_inst = Transaction.objects.create(user=user, product=product, quantity=qty, subtotal=total)
        trans_inst.save()

        product.quantity = product.quantity - int(qty)
        product.save()
        logger.info("User: "+ request.user.username+" purchase "+product.prodname+" X "+qty+" "+total+" successfully ")
        return redirect('/')

    return render(request, 'ecommerce/checkout.html', {'product': product})


def prodman(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes != "ProductManager":
        return error_403(request)

    product_list = Product.objects.all()
    logger.info("Product Manager: " + request.user.username + " viewed product lists")
    context = {
        'product_list': product_list,
    }
    return render(request, 'ecommerce/prodman.html', context)


def loginmanager(request):
    erroruser = False
    if request.user.is_authenticated:
        logger.info(str(request) + '  User:' + request.user.username + " logged out. ")
        logout(request)

    if request.method == 'POST':
        try:
            uname = request.POST['username']
        except:
            pass
        login(request)
        if request.user.is_authenticated:
            if request.user.usertypes == 'Administrator' or request.user.usertypes == 'ProductManager' or request.user.usertypes == 'AccountingManager':
                logger.info(str(request) + '  User:' + request.user.username + " login successfully !")
                user = User.objects.filter(username=request.POST['username'])[:1].get()
                print(user.usertypes)
                print(user.is_active)
                if not user.expired:
                    if user.usertypes == 'Administrator':
                        return redirect('/adminman/')
                    if user.usertypes == 'ProductManager':
                        return redirect('/prodman/')
                    if user.usertypes == 'AccountingManager':
                        return redirect('/acctman/')
            else:
                logger.warning(str(request) + '  User:' + uname + " login failed!")
                logout(request)
                erroruser = True

            return login(request)
        else:
            logger.warning(str(request) + '  User:' + uname + " login failed!")
            erroruser = True

    context ={
        'erroruser' : erroruser,
    }
    return render(request, 'ecommerce/loginmanager.html',context)


def adminman(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes != "Administrator":
        return error_403(request)
    logger.info("Administrator: " + request.user.username + " viewed admin page")
    return render(request, 'ecommerce/adminman.html')


def prodmng(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes != "Administrator":
        return error_403(request)
    logger.info("Administrator: " + request.user.username + " viewed product managers page")
    prodmanaccts = User.objects.filter(usertypes="ProductManager")
    context={
        'prodmanaccts':prodmanaccts
    }
    return render(request, 'ecommerce/prodmng.html',context)

def acctmng(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes != "Administrator":
        return error_403(request)
    logger.info("Administrator: " + request.user.username + " viewed accounting managers page")
    acctmanaccts = User.objects.filter(usertypes="AccountingManager")
    context={
        'acctmanaccts':acctmanaccts
    }
    return render(request, 'ecommerce/acctmng.html',context)

def changepass(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes == 'Customer':
        return error_403(request)
    context = {
        "alert": None
    }
    try:
        currpass = request.POST['currpass']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        BLACKLIST_PASSWORD = ['password', 'pass123', 'password123', 'admin', 'guest','123456','qwerty','12345678','qwertyuiop','google','zxcvbnm','111111','1234567890','123123','mynoob','18atcskd2w','1q2w3e4r','654321','letmein','football','iloveyou','welcome','monkey','abc123','passw0rd','dragon','starwars','123456789']
        
        if not user.check_password(currpass):
            context["alert"] = "Wrong password entered."
        elif pass1 != pass2:
            context["alert"] = "Passwords do not match."
        elif currpass == pass1:
            context["alert"] = "Your new password must differ from your previous password."
        elif pass1.lower() in BLACKLIST_PASSWORD:
            context["alert"] = "Invalid username/password."
        elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', pass1):
            context["alert"] = "The password must contain at least eight characters, at least one uppercase letter, one lowercase letter and one number."
        elif len(pass1) < 8:
            context["alert"] = "Password must be at least 8 characters long."
        elif (user.username).lower() in pass1.lower():
            context["alert"] = "Password should not contain your first name, last name, or username"
        elif (user.first_name).lower() in pass1.lower():
             context["alert"] = "Password should not contain your first name, last name, or username"
        elif (user.last_name).lower() in pass1.lower():
             context["alert"] = "Password should not contain your first name, last name, or username"
        elif user.check_password(currpass) and len(pass1) > 0 and len(pass2) > 0 and pass1 == pass2:
            user.set_password(pass1)
            user.save()
            logger.info("User: " + request.user.username +" "+ request.user.usertypes +" changed password successfully")
            return redirect('/loginmanager/')
        else:
            logger.warning("User: " + request.user.username +" "+ request.user.usertypes +" password was not changed")

    except : pass
    return render(request, 'ecommerce/changepass.html',context)


def proddelete(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes != "ProductManager":
        return error_403(request)
    ids = request.GET.getlist("ids[]")

    for id in ids:
        product = Product.objects.get(id=id)
        product.is_active = False
        product.save()
    logger.info("Product Manager: " + request.user.username + " discontinued the product " + product.prodname )
    return HttpResponse('Success')


def prodadd(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes != "ProductManager":
        return error_403(request)
    if (request.method == "POST"):
        name = request.POST["name"]
        desc = request.POST["description"]
        price = request.POST["price"]
        stock = request.POST["stock"]
        cat = request.POST["category"]

        product = Product()
        product.prodname = name
        product.description = desc
        product.category = cat
        product.price = price
        product.quantity = stock
        product.initialstock = stock
        product.is_active = True


        if (len(request.FILES) > 0):
            product.image = request.FILES["image"]

        product.save()
    logger.info("Product Manager: " + request.user.username + " added new product " + product.prodname)
    return HttpResponse('Success')


def prodedit(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes != "ProductManager":
        return error_403(request)
    if request.method == "POST":
        id = request.POST['id']
        name = request.POST["name"]
        desc = request.POST["description"]
        price = request.POST["price"]
        stock = request.POST["stock"]
        cat = request.POST["category"]

        product = Product.objects.get(id=id)
        product.prodname = name
        product.description = desc
        product.category = cat
        product.price = price
        product.initialstock = int(product.initialstock) + (int(stock) - int(product.quantity))
        product.quantity = stock

        if (len(request.FILES) > 0):
            product.image = request.FILES["image"]

        product.save()
        logger.info("Product Manager: " + request.user.username + " editted product information of " + product.prodname)

    return HttpResponse('Success')


def addp(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes != "Administrator":
        return error_403(request)
    context = {
        "alert": None
    }

    if request.method == "POST":
        first = request.POST["first"]
        last = request.POST["last"]
        username = request.POST["username"]
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]
        email = request.POST["email"]
        
        BLACKLIST_PASSWORD = ['password', 'pass123', 'password123', 'admin', 'guest','123456','qwerty','12345678','qwertyuiop','google','zxcvbnm','111111','1234567890','123123','mynoob','18atcskd2w','1q2w3e4r','654321','letmein','football','iloveyou','welcome','monkey','abc123','passw0rd','dragon','starwars','123456789']
        
        if len(first) > 0 and len(last) > 0 and len(username) > 0 and \
                len(password) > 0 and len(cpassword) > 0 and len(email) > 0:
            email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

            if password != cpassword:
                context["alert"] = "Passwords do not match."
            elif password.lower() in BLACKLIST_PASSWORD:
                context["alert"] = "Invalid username/password."
            elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password):
                context["alert"] = "The password must contain at least eight characters, at least one uppercase letter, one lowercase letter and one number."
            elif len(password) < 8:
                context["alert"] = "Password must be at least 8 characters long."
            elif username.lower() in password.lower():
                context["alert"] = "Password should not contain your first name, last name, or username"
            elif first.lower() in password.lower():
                 context["alert"] = "Password should not contain your first name, last name, or username"
            elif last.lower() in password.lower():
                 context["alert"] = "Password should not contain your first name, last name, or username"
            elif not email_pattern.match(email):
                context["alert"] = "Invalid email address"
            elif len(User.objects.filter(username=username)) > 0:
                context["alert"] = "The username already exists"
            elif len(User.objects.filter(email=email)) > 0:
                context["alert"] = "That email is already in use"
            else:
                pm_inst = User.objects.create_user(username=username,
                                                   email=email,
                                                   password=password, first_name=first, last_name=last,
                                                   usertypes='ProductManager', temporary=True)

                pm_inst.save()
                context["alert"] = "Product manager created"
                logger.info("Administrator: " + request.user.username + " successfully created product manager account " + pm_inst.username)

        else:
            context["alert"] = "Not enough information was given"
            logger.info("Administrator: " + request.user.username + " product manager account was not created not enough information was given")

    return render(request, 'ecommerce/addpman.html', context)


def adda(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes != "Administrator":
        return error_403(request)
    context = {
        "alert": None
    }

    if request.method == "POST":
        first = request.POST["first"]
        last = request.POST["last"]
        username = request.POST["username"]
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]
        email = request.POST["email"]
        
        BLACKLIST_PASSWORD = ['password', 'pass123', 'password123', 'admin', 'guest','123456','qwerty','12345678','qwertyuiop','google','zxcvbnm','111111','1234567890','123123','mynoob','18atcskd2w','1q2w3e4r','654321','letmein','football','iloveyou','welcome','monkey','abc123','passw0rd','dragon','starwars','123456789']

        if len(first) > 0 and len(last) > 0 and len(username) > 0 and \
                len(password) > 0 and len(cpassword) > 0 and len(email) > 0:
            email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

            if password != cpassword:
                context["alert"] = "Passwords do not match."
            elif password.lower() in BLACKLIST_PASSWORD:
                context["alert"] = "Invalid username/password."
            elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password):
                context["alert"] = "The password must contain at least eight characters, at least one uppercase letter, one lowercase letter and one number."
            elif len(password) < 8:
                context["alert"] = "Password must be at least 8 characters long."
            elif username.lower() in password.lower():
                context["alert"] = "Password should not contain your first name, last name, or username"
            elif first.lower() in password.lower():
                 context["alert"] = "Password should not contain your first name, last name, or username"
            elif last.lower() in password.lower():
                 context["alert"] = "Password should not contain your first name, last name, or username"
            elif not email_pattern.match(email):
                context["alert"] = "Invalid email address"
            elif len(User.objects.filter(username=username)) > 0:
                context["alert"] = "The username already exists"
            elif len(User.objects.filter(email=email)) > 0:
                context["alert"] = "That email is already in use"
            else:
                am_inst = User.objects.create_user(username=username,
                                                   email=email,
                                                   password=password, first_name=first, last_name=last,
                                                   usertypes='AccountingManager', temporary=True)

                am_inst.save()
                logger.info("Administrator: " + request.user.username + " successfully created account manager account " + am_inst.username)
                context["alert"] = "Accounting manager created"
        else:
            logger.info("Administrator: " + request.user.username + " accounting manager account was not created not enough information was given")
            context["alert"] = "Not enough information was given"

    return render(request, 'ecommerce/addaman.html', context)


def uacct(request):
    user = request.user
    if not user.is_authenticated or user.is_authenticated and user.usertypes != "Customer":
        return error_403(request)
    context = {
        "alert": None
    }
    if request.method == "POST":
        user = request.user
        try:
            fname = request.POST['fname']
            minitial = request.POST['minitial']
            lname = request.POST['lname']
            uname = request.POST['uname']
            email = request.POST['email']
            email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

            if len(fname) > 0 and len(minitial) == 1 and len(lname) > 0 and len(uname) > 0 and len(
                    email) > 0 and email_pattern.match(email):
                user.first_name = fname
                user.middle_initial = minitial
                user.last_name = lname
                user.username = uname
                user.email = email
                user.save()
                logger.info("User: " + request.user.username + " successfully edited personal profile information")
            else:
                logger.warning("User: " + request.user.username + " personal profile information was not edited")



        except:
            print('not account')

            try:
                
                currpass = request.POST['currpass']
                pass1 = request.POST['pass1']
                pass2 = request.POST['pass2']
                
                BLACKLIST_PASSWORD = ['password', 'pass123', 'password123', 'admin', 'guest','123456','qwerty','12345678','qwertyuiop','google','zxcvbnm','111111','1234567890','123123','mynoob','18atcskd2w','1q2w3e4r','654321','letmein','football','iloveyou','welcome','monkey','abc123','passw0rd','dragon','starwars','123456789']
                
                if not user.check_password(currpass):
                    context["alert"] = "Wrong password entered."
                elif pass1 != pass2:
                    context["alert"] = "Passwords do not match."
                elif currpass == pass1:
                    context["alert"] = "Your new password must differ from your previous password."
                elif pass1.lower() in BLACKLIST_PASSWORD:
                    context["alert"] = "Invalid username/password."
                elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', pass1):
                    context["alert"] = "The password must contain at least eight characters, at least one uppercase letter, one lowercase letter and one number."
                elif len(pass1) < 8:
                    context["alert"] = "Password must be at least 8 characters long."
                elif (user.username).lower() in pass1.lower():
                    context["alert"] = "Password should not contain your first name, last name, or username"
                elif (user.first_name).lower() in pass1.lower():
                     context["alert"] = "Password should not contain your first name, last name, or username"
                elif (user.last_name).lower() in pass1.lower():
                     context["alert"] = "Password should not contain your first name, last name, or username"
                elif user.check_password(currpass) and len(pass1) > 0 and len(pass2) > 0 and pass1 == pass2:
                    user.set_password(pass1)
                    user.save()
                    logger.info("User: " + request.user.username + " successfully changed user account password")
                    return redirect('/')
                else:
                        logger.warning("User: " + request.user.username + "user account password was not changed")

                
                
            except:
                print('not password')

                try:
                    bhouse_num = request.POST['bhouse_num']
                    bstreet = request.POST['bstreet']
                    bsubdivision = request.POST['bsubdivision']
                    bcity = request.POST['bcity']
                    bpc = request.POST['bpc']
                    bcountry = request.POST['bcountry']

                    shouse_num = request.POST['shouse_num']
                    sstreet = request.POST['sstreet']
                    ssubdivision = request.POST['ssubdivision']
                    scity = request.POST['scity']
                    spc = request.POST['spc']
                    scountry = request.POST['scountry']

                    if len(bhouse_num) > 0 and len(bstreet) > 0 and len(bsubdivision) > 0 and len(bcity) > 0 and len(
                            bpc) > 0 and len(bcountry) > 0 and len(shouse_num) > 0 and len(sstreet) > 0 and len(
                        ssubdivision) > 0 and len(scity) > 0 and len(spc) > 0 and len(scountry) > 0:
                        user.bhouse_num = bhouse_num
                        user.bstreet = bstreet
                        user.bsubdivision = bsubdivision
                        user.bcity = bcity
                        user.bpc = bpc
                        user.bcountry = bcountry

                        user.shouse_num = shouse_num
                        user.sstreet = sstreet
                        user.ssubdivision = ssubdivision
                        user.scity = scity
                        user.spc = spc
                        user.scountry = scountry

                        user.save()
                        logger.info("User: " + request.user.username + " successfully edited billing/shipping address information")
                    else:
                        logger.warning("User: " + request.user.username + " billing/shipping address information was not edited")

                except:
                    print('not address')

    return render(request, 'ecommerce/uacct.html', context)

def product(request, product_id):
    product_obj = Product.objects.filter(id=product_id)[:1].get()
    reviews_obj = Review.objects.filter(product=product_obj)
    t_obj = None
    erroruser = False
    error_similar = False
    error_pblack = False
    error_length = False
    error_alpha = False
    error_match = False
    error_exists = False
    
    BLACKLIST_PASSWORD = ['password', 'pass123', 'password123', 'admin', 'guest','123456','qwerty','12345678','qwertyuiop','google','zxcvbnm','111111','1234567890','123123','mynoob','18atcskd2w','1q2w3e4r','654321','letmein','football','iloveyou','welcome','monkey','abc123','passw0rd','dragon','starwars','123456789']
    BLACKLIST_USERNAME = [ 'admin', 'administrator', 'root', 'system', 'guest','operator','super','gg','test1','testing','user','111111','123456','12345678','abc123','abramov','account','accounting','ad','adm','adver','advert','advertising','afanasev','agafonov','agata','Baseball','business','company','contact','contactus','design','director','dragon','manager','marketing','mysql','oracle','password','postmaster','qwerty','test','user','webmaster']
    
    if request.user.is_authenticated:
    	t_obj = Transaction.objects.filter(user=request.user, product=product_obj)

    if request.method == 'POST':
        regform = RegistrationForm(request.POST)
        revform = ReviewForm(request.POST)
        print("REQUEST POST")
        if regform.is_valid():
            password=regform.cleaned_data['password1']
            print("FORM VALID")
            regform.save()
            return redirect('/')
        
        try:
            fname_passed =  regform.cleaned_data.get('first_name')
            lname_passed =  regform.cleaned_data.get('last_name')
            username_passed = request.POST['username']
            password_passed = regform.cleaned_data.get('password1')
            password2_passed = request.POST['password2']
        except:
            pass
        
        if revform.is_valid():
            print("REVFORM VALID")
            rev = revform.save(commit=False)
            rev.product = product_obj
            rev.user = request.user
            rev.save()
            logger.info("User: " + request.user.username + " wrote a review on product " + product_obj.prodname)
            
        try:uname = request.POST['username']
        except:pass
        login(request)
        if request.user.is_authenticated:
            if request.user.usertypes == 'Customer':
                logger.info(str(request) + '  User:' + request.user.username + " login successfully!")
            else:
                logger.warning(str(request) + '  User:' + uname + " login failed!")
                logout(request)
                erroruser = True

            return login(request)
        elif username_passed and password_passed and fname_passed and lname_passed:
            
            # ALPHANUMERIC
            if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password_passed):
                error_alpha = True
                
            # PASSWORD IS BLACKLISTED
            elif password_passed.lower() in BLACKLIST_PASSWORD:
                error_pblack = True            
                
            elif username_passed.lower() in BLACKLIST_USERNAME:
                error_pblack = True
                
            # MIN_LENGTH IS 8
            elif len(password_passed) < 8:
                error_length = True
            
            # MATCH?
            elif password_passed != password2_passed:
                error_match = True

            # EXISTING USERNAME
            elif len(User.objects.filter(username=username_passed)) > 0:
                error_exists = True
            
            # USERNAME, FNAME, LNAME != PASSWORD
            elif username_passed.lower() in password_passed.lower():
                error_similar = True

            elif fname_passed.lower() in password_passed.lower():
                error_similar = True

            elif lname_passed.lower() in password_passed.lower():
                error_similar = True
        else:
            logger.warning(str(request) + '  User:' + uname + " login failed!")
            erroruser = True

    regform = RegistrationForm()
    revform = ReviewForm()
    context = {
        'error_length': error_length,
        'error_alpha': error_alpha,
        'error_pblack': error_pblack,
        'error_similar': error_similar,
        'error_exists': error_exists,
        'error_match': error_match,
        'erroruser': erroruser,
        'regform': regform,
        'revform': revform,
        'product_obj': product_obj,
        'reviews_obj': reviews_obj,
        't_obj': t_obj,
    }
    return render(request, 'ecommerce/product.html', context)
    




