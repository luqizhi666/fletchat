import flet as ft
from supabase import create_client, Client

url = "https://supabase.022408.xyz"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zc2pheHVvYWhyam5xb3BiemVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3ODc4NDMsImV4cCI6MjA3MTM2Mzg0M30.hhr57_wbhM6_-4Z63vPugliQb-i3Fg4J90HGT7okEZY"  # 用户端用 anon key
supabase: Client = create_client(url, key)



def main(page):

    page.adaptive = True

    page.appbar = ft.AppBar(
        leading=ft.TextButton("New", style=ft.ButtonStyle(padding=0)),
        title=ft.Text("Adaptive AppBar"),
        actions=[
            ft.IconButton(ft.CupertinoIcons.ADD, style=ft.ButtonStyle(padding=0))
        ],
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),
    )


    def Barchange(e):
        pagecontainer.content=pages[page.navigation_bar.selected_index]
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
        words.value = "注册成功！" + f"{response}"
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