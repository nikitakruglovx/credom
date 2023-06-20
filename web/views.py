from django.db.utils import IntegrityError
from passlib.hash import django_pbkdf2_sha256, pbkdf2_sha256
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from bs4 import BeautifulSoup
from web3 import Web3
from PIL import Image

from .models import CloudFiles, Folder, Users, Items, News
from .forms import CloudFilesForm, FeedbackForm, FolderForm, ItemForm, UsersForm
from .connect import cursor, connection

import requests
import zipfile
import os
import qrcode as qrcode
import uuid
import telebot

token = '5359114697:AAEhjqXdqQ-n0TjWVGpzOc76K3gMI5B0iYc'
chat_id = '5310768382'

bot = telebot.TeleBot(token)

def index_view(request):
    return render(request, 'index/index.html')

def aboutproject_view(request):
    return render(request, 'index/about.html')

@login_required
def home_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query, text_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/home.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                item_list = Items.objects.all()
                context = {
                    'item_list': item_list
                }
                return render(request, 'account/home.html', context)
            else:
                messages.error(request, 'Неправельный логин или пароль')
                return render(request, 'auth/login.html')
        except:
            messages.error(request, 'Произошла какая то ошибка, попробуйте ещё раз')   
    return render(request, 'auth/login.html')

def register_view(request):
    success = {'Успешная регистрация!'}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        repasswd = request.POST['repasswd']
        if len(password) > 8:
            if password == repasswd:
                try:
                    try:
                        uu_id = uuid.uuid1()
                        MNEMONIC: str = generate_mnemonic(language="english", strength=128)
                        bip44: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
                        bip44.from_mnemonic(mnemonic=MNEMONIC, language="english")
                        bip44.clean_derivation()

                        bip44_derivation: BIP44Derivation = BIP44Derivation(cryptocurrency=EthereumMainnet, account=0, change=False, address=0)
                        bip44.from_path(path=bip44_derivation)
                        private_key = '0x' + bip44.private_key()
                        address = bip44.address()
                        img = qrcode.make(address)
                        newadduser = Users.objects.create_superuser(username=username, password=password, uu_id=uu_id, wallet_address=address, seed=MNEMONIC, privatekey=private_key)
                        img.save(f'media/qrcode/{username}.png')
                        newadduser.save()
                        return render(request, 'auth/registration.html', {'success': success})
                    except IntegrityError:
                        messages.error(request, 'Такой пользователь уже существует')
                except ValueError:
                    messages.error(request, 'Пожалуйста, заполните все поля')
            else:
                messages.error(request, 'Пароли не совпадают')
        else:
            messages.error(request, 'Пароль должен содержать минимум 8 символов')
    return render(request, 'auth/registration.html')

def logout_view(request):
    logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                item_list = Items.objects.all()
                context = {
                    'item_list': item_list
                }
                return render(request, 'account/home.html', context)
            else:
                messages.error(request, 'Неправельный логин или пароль')
                return render(request, 'auth/login.html')
        except:
            messages.error(request, 'Произошла какая то ошибка, попробуйте ещё раз')
    return render(request, 'auth/login.html')
    
@login_required
def profile_view(request):
    success = {'Пароль успешно изменён!'}
    success_send = {'Отправлено'}
    if request.method == 'POST' and 'btnsend' in request.POST:
        try:
            eth_send_address = request.POST['eth_send_address']
            eth_send_amount = request.POST['eth_send_amount']

            web3 = Web3(Web3.HTTPProvider('https://ethereumnodelight.app.runonflux.io'))
            user_address = Users.objects.get(wallet_address=request.user.wallet_address).wallet_address
            account_1 = str(user_address)
            user_privatekey = Users.objects.get(privatekey=request.user.privatekey).privatekey
            private_key1 = str(user_privatekey)
            account_2 = str(eth_send_address)
            nonce = web3.eth.getTransactionCount(account_1)
            tx = {
                'nonce': nonce,
                'to': account_2,
                'value': web3.toWei(float(eth_send_amount), 'ether'),
                'gas': 2000000,
                'gasPrice': web3.toWei('50', 'gwei')
            }
            signed_tx = web3.eth.account.sign_transaction(tx, private_key1)
            web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            return render(request, 'account/profile.html', {'success': success_send})
        except:
            messages.error(request, 'Не удалось отправить транзакцию, попробуйте ещё раз')
    if request.method == 'POST' and 'btnsave' in request.POST:
        old_password = request.POST['oldpasswd']
        new_password = request.POST['newpasswd']
        replace_password = request.POST['repasswd']
        user_password = Users.objects.get(password=request.user.password).password
        check_hash = check_password(old_password, user_password)
        if len(new_password) == 0:
            messages.error(request, 'Заполните пожалуйста все поля')
        elif len(replace_password) == 0:
            messages.error(request, 'Заполните пожалуйста все поля')
        elif len(old_password) == 0:
            messages.error(request, 'Заполните пожалуйста все поля')
        else:
            if check_hash is True:
                if len(new_password) > 8:
                    if new_password == replace_password:
                        hash = django_pbkdf2_sha256.hash(new_password)
                        id_user_get = Users.objects.get(uu_id=request.user.uu_id).uu_id
                        cursor.execute(f"UPDATE web_users SET password = '{hash}' WHERE uu_id = '{str(id_user_get)}'")
                        connection.commit()
                        return render(request, 'account/profile.html', {'success': success})
                    else:
                        messages.error(request, 'Ошибка, пароли не совпадают!')
                else:
                    messages.error(request, 'К сожалению пароль должен быть минимум 8 символов!')
            else:
                messages.error(request, 'Неверный пароль')
    try:
        address = Users.objects.get(wallet_address=request.user.wallet_address).wallet_address
        url = f'https://www.blockchain.com/eth/address/{address}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
        Response = requests.get(url, headers=headers)
        wallet = BeautifulSoup(Response.content, 'html.parser')
        convert = wallet.findAll("span", {"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0","class": "eQTRKC"})
        BL = convert[6].text
    except:
        address = Users.objects.get(wallet_address=request.user.wallet_address).wallet_address
        url = f'https://www.blockchain.com/eth/address/{address}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
        Response = requests.get(url, headers=headers)
        wallet = BeautifulSoup(Response.content, 'html.parser')
        convert = wallet.findAll("span", {"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0","class": "eQTRKC"})
        BL = convert[6].text
    balance = str(BL).rstrip('ETH')
    get_prof = Users.objects.all()
    context = {
        'get_prof': get_prof,
        'items': Items.objects.filter(author=request.user),
        'items_buy': Items.objects.filter(orders_buyers=request.user),
        'balance': balance
    }
    return render(request, 'account/profile.html', context)

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        # address = Users.objects.get(wallet_address=request.user.wallet_address).wallet_address
        # url = f'https://www.blockchain.com/eth/address/{address}'
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
        # Response = requests.get(url, headers=headers)
        # wallet = BeautifulSoup(Response.content, 'html.parser')
        # convert = wallet.findAll("span", {"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0","class": "eQTRKC"})
        # BL = convert[6].text
        # balance = str(BL).rstrip('ETH')
        # if float(balance) < float(0.00669825):
        #     messages.error(request, 'На вашем балансе не хватает средств для добавления товара!')
        # else:
        if form.is_valid():
            form_G = form.save(commit=False)
            form_G.author = request.user
            archive = form_G.archive_file
            filelink = form_G.file_link
            if archive == None:
                if filelink == None:
                    messages.error(request, 'Вы не добавили файл товара, добавьте файл на товар загрузив его или добавьте ссылку на товар')
                if filelink.startswith('https://'):
                    form_G.save()
                    return redirect('home')
                else:
                    messages.error(request, 'Заполните корректно ссылку на товар')
            else:
                if str(f"{archive}").endswith('.zip'):
                    form_G.save()
                    zf = zipfile.ZipFile(f'media/{archive}')
                    for zinfo in zf.infolist():
                        is_encrypted = zinfo.flag_bits & 0x1 
                        if is_encrypted:
                            messages.error(request, 'Архив под паролем: загружать можно только архиве без пароля')
                            os.remove(f'media/{archive}')
                            form_G.delete()
                            return redirect('additem')
                        else:
                            success = {'Объект успешно размещён'}
                            return render(request, 'account/home.html', {'success': success})
                else:
                    messages.error(request, 'Вы можете добавить только ZIP архивы')
        else:
            messages.error(request, 'Не удалось добавить, какая-то ошибка')
            return redirect('additem')

    form = ItemForm()
    try:
        address = Users.objects.get(wallet_address=request.user.wallet_address).wallet_address
        url = f'https://www.blockchain.com/eth/address/{address}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
        Response = requests.get(url, headers=headers)
        wallet = BeautifulSoup(Response.content, 'html.parser')
        convert = wallet.findAll("span", {"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0","class": "eQTRKC"})
        BL = convert[6].text
    except:
        address = Users.objects.get(wallet_address=request.user.wallet_address).wallet_address
        url = f'https://www.blockchain.com/eth/address/{address}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
        Response = requests.get(url, headers=headers)
        wallet = BeautifulSoup(Response.content, 'html.parser')
        convert = wallet.findAll("span", {"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0","class": "eQTRKC"})
        BL = convert[6].text
    balance = str(BL)
    total = float(balance.rstrip('ETH')) < float(0.00669825)
    total_upload = float(balance.rstrip('ETH')) - float(0.00669825)
    data = {
        'form': form,
        'balance': balance,
        'total': total,
        'total_upload': total_upload
    }
    return render(request, 'account/additem.html', data)

@login_required
def sitesandweb_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/sitesandweb.html', context)

@login_required
def itembuy_view(request, id):
    get_item_list = Items.objects.get(id=id)
    context = {
    'get_item_list': get_item_list
    }
    if request.method == 'POST' and 'btnbuy' in request.POST:
        try:
            address = Users.objects.get(wallet_address=request.user.wallet_address).wallet_address
            url = f'https://www.blockchain.com/eth/address/{address}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
            Response = requests.get(url, headers=headers)
            wallet = BeautifulSoup(Response.content, 'html.parser')
            convert = wallet.findAll("span", {"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0","class": "eQTRKC"})
            BL = convert[6].text
            balance = str(BL).rstrip('ETH')
        except:
            address = Users.objects.get(wallet_address=request.user.wallet_address).wallet_address
            url = f'https://www.blockchain.com/eth/address/{address}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
            Response = requests.get(url, headers=headers)
            wallet = BeautifulSoup(Response.content, 'html.parser')
            convert = wallet.findAll("span", {"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0","class": "eQTRKC"})
            BL = convert[6].text
            balance = str(BL).rstrip('ETH')
        price = Items.objects.get(pk=id).price_item
        if float(balance) >= float(price):
            user = request.user
            item_author = Items.objects.get(pk=id).author
            if user == item_author:
                messages.error(request, 'Вы не можете купить свой товар')
            else:
                try:
                    item_check = Items.objects.get(pk=id)
                    user_check = Users.objects.get(pk=request.user.pk)
                    success = {'Объект куплен!'}
                    if user_check in item_check.orders_buyers.all():
                        messages.error(request, 'Вы уже купили данный объект')
                    else:
                        item_author_address = Items.objects.get(pk=id).author
                        item_amount = Items.objects.get(pk=id).price_item
                        author_address = item_author_address.wallet_address

                        def toFixed(commission, digits=0):
                            return f"{commission:.{digits}f}"

                        commission = float(item_amount) / 100 * 5
                        commission_full = toFixed(commission, 8)
                        item_amount_full = float(item_amount) - float(commission_full)


                        eth_send_address = str(author_address)
                        eth_send_amount = str(toFixed(item_amount_full, 8))

                        if item_amount <= float(0.00000000):
                            item_buyers = Items.objects.get(pk=id)
                            item_buyers.orders_buyers.add(user)
                            return render(request, 'account/profile.html', {'success': success})
                        else:
                            try:
                                web3 = Web3(Web3.HTTPProvider('https://ethereumnodelight.app.runonflux.io'))
                                user_address = Users.objects.get(wallet_address=request.user.wallet_address).wallet_address
                                account_1 = str(user_address)
                                user_privatekey = Users.objects.get(privatekey=request.user.privatekey).privatekey
                                private_key1 = str(user_privatekey)
                                account_2 = str(eth_send_address)
                                nonce = web3.eth.getTransactionCount(account_1)
                                tx = {
                                    'nonce': nonce,
                                    'to': account_2,
                                    'value': web3.toWei(float(eth_send_amount), 'ether'),
                                    'gas': 2000000,
                                    'gasPrice': web3.toWei('50', 'gwei')
                                }
                                signed_tx = web3.eth.account.sign_transaction(tx, private_key1)
                                web3.eth.sendRawTransaction(signed_tx.rawTransaction)

                                # web3 = Web3(Web3.HTTPProvider('https://ethereumnodelight.app.runonflux.io'))
                                # user_address = Users.objects.get(wallet_address=request.user.wallet_address).wallet_address
                                # account_1 = str(user_address)
                                # user_privatekey = Users.objects.get(privatekey=request.user.privatekey).privatekey
                                # private_key1 = str(user_privatekey)
                                # account_2 = ''
                                # nonce = web3.eth.getTransactionCount(account_1)
                                # tx = {
                                #     'nonce': nonce,
                                #     'to': account_2,
                                #     'value': web3.toWei(float(commission_full), 'ether'),
                                #     'gas': 2000000,
                                #     'gasPrice': web3.toWei('50', 'gwei')
                                # }
                                # signed_tx = web3.eth.account.sign_transaction(tx, private_key1)
                                # web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                                item_buyers = Items.objects.get(pk=id)
                                item_buyers.orders_buyers.add(user)
                            except:
                                messages.error(request, 'Произошла техническая ошибка')
                        return render(request, 'account/profile.html', {'success': success, 'item_author': item_author})
                except:
                    messages.error(request, 'Произошла ошибка из-за нагрузки, попробуйте ещё раз')
        else:
            messages.error(request, 'Не хватает средтств, для покупки пополните ваш баланс')
    if request.method == 'POST' and 'btndel' in request.POST:
        delete_item = Items.objects.get(id=id)
        success_del = {'Объект успешно удалён, все его данные и файлы унечтожены.'}
        if request.user == delete_item.author:
            try:
                os.remove(f'media/{delete_item.archive_file}')
                delete_item.delete()
                return render(request, 'account/buyview.html', {'success': success_del})
            except IsADirectoryError:
                delete_item.delete()
                return render(request, 'account/buyview.html', {'success': success_del})
        else:
            messages.error(request, 'Ошибка, что ты делаешь?')
    return render(request, 'account/buyview.html', context)

@login_required
def account_view(request, username):
    user = get_object_or_404(Users, username=username)
    if request.user == user:
        return redirect('profile')
    else:
        username_usr = Users.objects.get(username=username)
        context = {
            'user_account': username_usr,
            'items': Items.objects.filter(author=user)
        }
        return render(request, 'account/@profile.html', context)

@login_required
def editprofile_view(request):
    up_info = Users.objects.get(username=request.user)
    form = UsersForm(instance=up_info)
    if request.method == 'POST':
        form = UsersForm(request.POST, request.FILES, instance=up_info)
        if form.is_valid():
            form_G = form.save(commit=False)
            banner = form_G.background_profile
            form_G.save()
            img = Image.open(f'media/{banner}')
            width = 1599
            height = 450
            resized_img = img.resize((width, height))
            resized_img.save(f'media/{banner}')
            return redirect('profile')
        else:
            return redirect('home')
    data = {
        'form': form
    }
    return render(request, 'account/editprofile.html', data)

@login_required
def cloud_view(request):
    if request.method == 'POST' and 'btncloud' in request.POST:
        form = CloudFilesForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form_G = form.save(commit=False)
            form_G.author_files = request.user
            form_G.name_file = str(form_G.file)
            form_G.save()

            def convert_bytes(num):
                for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                    if num < 1024.0:
                        return "%3.1f %s" % (num, x)
                    num /= 1024.0

            def file_size(file_path):
                if os.path.isfile(file_path):
                    file_info = os.stat(file_path)
                    return convert_bytes(file_info.st_size)
                    
            file_path = f'media/{form_G.file}'
            size = file_size(file_path)
            form_G.total_size = size
            form_G.save()
    if request.method == 'POST' and 'btnfolder' in request.POST:
        form2 = FolderForm(request.POST)
        if form2.is_valid():
             new_folder = form2.save(commit=False)
             new_folder.author_folder = request.user
             new_folder.save()
    form2 = FolderForm()
    form = CloudFilesForm(request.user, request.POST, request.FILES)
    folder = Folder.objects.filter(author_folder=request.user)
    cloud_files = CloudFiles.objects.filter(author_files=request.user)
    data = {
        'form': form,
        'cloud_files': cloud_files,
        'form2': form2,
        'folder': folder
    }
    return render(request, 'account/cloud.html', data)

@login_required
def cloudid_view(request, id):
    folder_view = Folder.objects.filter(id=id, author_folder=request.user)
    folder_files = CloudFiles.objects.filter(folder=id)
    filedel =  CloudFiles.objects.all().filter(folder=id)
    success = {'Удалено!'}
    if request.method == 'POST' and 'btnclouddel' in request.POST:
        try:
            while True:
                for i in filedel:
                    os.remove(f'media/{i.file}')
                folder_view.delete()
                return render(request, 'account/cloud.html', {'success': success})
        except IsADirectoryError:
           folder_view.delete() 
           return render(request, 'account/cloud.html', {'success': success})
    context = {
        'folder_view': folder_view,
        'folder_files': folder_files
    }
    return render(request, 'account/cloudfolder.html', context)

@login_required
def about_view(request):
    success = {'Отправленно!'}
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            contact = form.cleaned_data['contact']
            messagess = form.cleaned_data['messagess']
            data = {
                f'Пользователь: {request.user}\n'
                f'Контакт для связи: {contact}\n'
                f'Сообщение: {messagess}'
            }
            bot.send_message(chat_id, data)
            return render(request, 'account/about.html', {'success': success, 'form': form})
        else:
            messages.error(request, 'Не верно решена капча')
    form = FeedbackForm()
    context = {
        'form': form
    }
    return render(request, 'account/about.html', context)

@login_required
def help_view(request):
    return render(request, 'account/help.html')

@login_required
def news_view(request):
    news = News.objects.all()
    context = {
        'news': news
    }
    return render(request, 'account/news.html', context)

@login_required
def scripts_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/scripts.html', context)

@login_required
def bots_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/bots.html', context)

@login_required
def mobile_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/mobileapp.html', context)

@login_required
def software_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/desktops.html', context)

@login_required
def templates_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query, text_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/front-templates.html', context)

@login_required
def logotype_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/logos.html', context)

@login_required
def treedmodels_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/3dmodels.html', context)

@login_required
def books_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/books.html', context)

@login_required
def scripts_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/scripts.html', context)

@login_required
def scripts_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/scripts.html', context)

@login_required
def courses_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        item_list = Items.objects.filter(name_item=search_query)
    else:
        item_list = Items.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'account/courses.html', context)