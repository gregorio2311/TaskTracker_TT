import flet as ft

def main(page: ft.Page):
    def login_click(e):
        # Aquí iría la lógica para validar el inicio de sesión
        # Por ahora, solo redirigimos a la página del calendario
        page.controls.clear()
        create_calendar_page(page)

    # Controles para el login
    txt_username = ft.TextField(label="Nombre de usuario", autofocus=True)
    txt_password = ft.PasswordField(label="Contraseña")
    btn_login = ft.Button("Iniciar sesión", on_click=login_click)

    # Agregando controles a la página
    page.add(txt_username, txt_password, btn_login)

def create_calendar_page(page: ft.Page):
    # Aquí construirás la interfaz del calendario
    page.add(ft.Text("Bienvenido al Calendario"))

# Ejecutar la aplicación
ft.app(target=main)
