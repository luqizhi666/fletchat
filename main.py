import flet as ft
from supabase import create_client, Client
from flet.security import encrypt, decrypt
import uuid
url = "https://supabase.022408.xyz"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zc2pheHVvYWhyam5xb3BiemVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3ODc4NDMsImV4cCI6MjA3MTM2Mzg0M30.hhr57_wbhM6_-4Z63vPugliQb-i3Fg4J90HGT7okEZY"  # 用户端用 anon key
supabase: Client = create_client(url, key)



def main(page):
    #login state
    if page.client_storage.contains_key("Uid"):
        SECRET_KEY = page.client_storage.get("Uid")
        if page.client_storage.contains_key("supabase_jwt"):
            encrypted_jwt = page.client_storage.get("supabase_jwt")
            jwt_token = decrypt(encrypted_jwt, SECRET_KEY)
            userinfo = supabase.auth.get_user(jwt_token)
            print(userinfo)


    else:
        Uid = uuid.uuid4()
        SECRET_KEY = Uid.hex
        page.client_storage.set("Uid", Uid.hex)


    def logorsign(e):
        if page.appbar.actions[1].text == "注册":
            page.appbar.actions[1].text = "登录"
            submit.text = "注册"
            account_page.controls[0].value = "注册"
            words.value = "注册即表示您同意我们的条款和隐私政策"
            submit.on_click = signup

        elif page.appbar.actions[1].text == "登录":
            page.appbar.actions[1].text = "注册"
            submit.text = "登录"
            account_page.controls[0].value = "登录"
            words.value = "登录即表示您同意我们的条款和隐私政策"
            submit.on_click = login

        page.update()


    page.adaptive = True

    pagetitle=["主页", "通讯录", "我的"]
    page.appbar = ft.AppBar(
        leading=ft.TextButton("New", style=ft.ButtonStyle(padding=0)),
        title=ft.Text("消息"),
        actions=[
            ft.IconButton(ft.CupertinoIcons.ADD, style=ft.ButtonStyle(padding=0)),
            ft.TextButton(text="登录",on_click=logorsign)
        ],
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),
    )


        
    def Barchange(e):
        pagecontainer.content=pages[page.navigation_bar.selected_index]
        page.appbar.title=ft.Text(pagetitle[page.navigation_bar.selected_index])
        if page.navigation_bar.selected_index==2:
            page.appbar.actions[1].visible=True
        else:
            page.appbar.actions[1].visible=False
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="主页"),
            ft.NavigationBarDestination(icon=ft.Icons.CONTACTS, label="通讯录"),
            ft.NavigationBarDestination(
                icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                selected_icon=ft.Icons.ACCOUNT_CIRCLE,
                label="我的",
            ),
        ],
        border=ft.Border(
            top=ft.BorderSide(color=ft.CupertinoColors.SYSTEM_GREY2, width=0)
        ),
        on_change=Barchange,
    )

    homepage=ft.Column(
                [
                    ft.Checkbox(value=False, label="Dark Mode"),
                    ft.Text("First field:"),
                    ft.TextField(keyboard_type=ft.KeyboardType.TEXT),
                    ft.Text("Second field:"),
                    ft.TextField(keyboard_type=ft.KeyboardType.TEXT),
                    ft.Switch(label="A switch"),
                    ft.FilledButton(content=ft.Text("Adaptive button")),
                    ft.Text("Text line 1"),
                    ft.Text("Text line 2"),
                    ft.Text("Text line justdo it"),
                ]
            )
    
    contact_page=ft.Text("Page 2")



    def signup(e):
        response = supabase.auth.sign_up(
            {
                "email": f"{email.value}",
                "password": f"{password.value}",
            }
        )
        print(response)
        if response.user is not None:
            words.value = "注册成功！" + f"{response}"
            if response.user.email_confirmed_at is None:
                words.value += "请前往邮箱进行验证！"
            else:
                jwt_token = response.session.access_token  # 登录凭证
                encrypted_jwt = encrypt(jwt_token, SECRET_KEY)
                page.client_storage.set("supabase_jwt", encrypted_jwt) # 在本地储存加密过的jwt
        else:
            words.value = "注册失败！" + f"{response}"
        page.update()

    def login(e):
        try:
            response = supabase.auth.sign_in_with_password(
                {"email": email.value, "password": password.value}
            )
            print(response)
            # 登录成功后的处理
        except Exception as ex:
            words.value = "登录失败：邮箱或密码错误"
            print(f"登录失败: {ex}")
            page.update()
            print(response)
        if response.user is not None:
            words.value = "登录成功！" + f"{response}"
            if response.user.email_confirmed_at is None:
                words.value += "请前往邮箱进行验证！"
            else:
                jwt_token = response.session.access_token  # 登录凭证
                encrypted_jwt = encrypt(jwt_token, SECRET_KEY)
                page.client_storage.set("supabase_jwt", encrypted_jwt) # 在本地储存加密过的jwt
        else:
            words.value = "登录失败！" + f"{response}"
        page.update()
    
    
    email = ft.TextField(label="邮箱", autofocus=True)
    password = ft.TextField(label="密码", password=True)
    tiaokuancheckbox = ft.Checkbox(label="您已阅读且同意条款")
    submit = ft.FilledButton("注册", disabled=True, on_click=signup)  # on_click will be set later
    words=ft.Text("注册即表示您同意我们的条款和隐私政策", size=10, color=ft.Colors.GREY)
    account_page = ft.Column([
        ft.Text("注册"),
        email,
        password,
        tiaokuancheckbox,
        submit,
        words
    ])




    def check(e):
        if all([email.value, password.value, tiaokuancheckbox.value]):
            submit.disabled = False
            page.update()
        else:
            submit.disabled = True
            page.update()
    


    email.on_change = check
    password.on_change = check
    tiaokuancheckbox.on_change = check

    pages=[homepage, contact_page, account_page]
    pagecontainer=ft.Container(pages[0])
    page.add(
        ft.SafeArea(
            pagecontainer
        )
    )


ft.app(main)