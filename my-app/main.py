import flet as ft

def main(page: ft.Page):
    page.title = "Inicio de Sesión"

    # Function to handle the button click event
    def on_login_click(e):
        print("Botón de inicio de sesión presionado")

    # Create a user image widget with a placeholder for now
    user_image = ft.Image(src="url_or_path_to_user_image", width=100, height=100)

    # Create text fields for username and password
    username = ft.TextField(label="Nombre de Usuario", autofocus=True)
    password = ft.TextField(label="Contraseña", password=True)

    # Create a button for submitting the login form
    login_button = ft.ElevatedButton(text="Iniciar Sesión", on_click=on_login_click)

    # Create a column for the form elements
    form_elements = ft.Column(controls=[
        user_image, username, password, login_button
    ])

    # Create a row that centers the column on the page
    centered_row = ft.Row(controls=[
        ft.Expanded(), form_elements, ft.Expanded()
    ], expand=True)

    # Add some padding around the row to push it to the center of the page vertically
    centered_content = ft.Padding(padding=ft.EdgeInsets.all(16), content=centered_row)

    # Add the padded row to the page
    page.add(centered_content)

ft.app(target=main)
