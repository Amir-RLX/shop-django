# shop-django
 # تنظیمات گیتهاب
اگر از قبل گیتهاب را برای اتصال ssh تنظیم نکرده اید در ترمینال لینوکس این دستور را اجرا کنید:
```
cat ~/.ssh/id_rsa.pub
```
اگر خطا داد این دستور را اجرا کنید و همه سوالات را خالی اینتر کنید و بعد از آن دستور قبلی را دوباره امتحان کنید  
(**دقت کنید این دستور را فقط به شرطی اجرا کنید که دستور قبلی خطای file not found داده باشد وگرنه کلید قبلی ssh شما بازنویسی میشود**):
```
ssh-keygen
```

اگر خروجی دریافت کردید خروجی را کپی کنید و در بخش تنظیمات سایت گیتهاب وارد شده و در پنل کناری در بخش SSH Keys یک کلید جدید بسازید و مقدار کپی شده را آنجا پیست کنید.

سپس میتوانید پروژه رو کلون کنید:
```
git clone git@github.com:anisa-django/adv-dj-1402-01.git
```


# راه اندازی اولیه
برای راه اندازی اولیه پروژه ابتدا یک virtualenv بسازید:
```
virtualenv -p python3 venv

```
و پس از فعال سازی آن پیش نیاز ها را با استفاده از دستور زیر نصب کنید:
```
pip install -r requirements.txt
```
# وارد کردن پروژه در محیط پایچارم
در پایچارم گذینه `Open Project` را بزنید و فولدر اصلی گیت که کلون کردید را انتخاب کنید بعد از باز شدن پروژه از طریق منوی `File > Settings` به بخش `Project > Project Interpreter` یک اینترپرتر دستی اضافه کنید و نوع را `Virtualenv` از نوع `Existing` انتخاب کنید و برای انتخاب کردنش فایل `bin/python` از فولدر `venv` که در مرحله قبل ساختید را انتخاب کنید. 

سپس در همان صفحه تنظیمات پایچارم گذینه `Language And Frameworks > Django` را انتخاب کرده و تیک `Enabled` اش را بزنید. برای Django Project Root فولدر `boomarkmanager` از داخل پروژه را انتخاب کنید و برای Settings مقدار `boomarkmanager/settings.py` را بزنید

در نهایت از منوی Run گذینه Edit Configurations را زده و با زدن علامت `+` یک تنظیم جدید از نوع `Django Server` ایجاد کنید و نام دلخواه برای آن بگذارید و OK کنید.

# نصب داکر روی لینوکس اوبونتو
برای نصب داکر بر روی لینوکس های مبتنی بر دبیان، در صورتی که از قبل داکر را نصب نکرده اید،
این دستورات را به ترتیب اجرا کنید:
```
sudo apt update

sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

sudo apt install docker-ce

sudo usermod -aG docker ${USER}
```
سپس یکبار سیستم را ری استارت کنید


## راه اندازی پستگرس
در ترمینال این دستور را وارد کنید تا پستگرس اجرا شود:
```
docker compose -f docker/docker-compose.yml up -d
```




```export $(cat env | xargs)```

```https://docs.djangoproject.com/en/4.2/ref/models/fields/```
