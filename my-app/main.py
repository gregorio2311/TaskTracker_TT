import flet
import json
import urllib.request
from flet import (
    Checkbox, Column, FloatingActionButton, IconButton, Page,
    Row, Tab, Tabs, TextField, UserControl, colors, icons, Text,
)

# URL del backend de Flask (reemplaza esto con tu URL real del servidor Flask)
BACKEND_URL = "http://localhost:5000"

def send_request(url, method, data=None):
    req_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=req_data, headers={'Content-Type': 'application/json'}, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        error_message = error.read().decode()
        print(f"HTTP Error {error.code}: {error_message}")
        return {"error": error_message}
    except urllib.error.URLError as error:
        print(f"URL Error: {error.reason}")
        return {"error": str(error.reason)}
        
class Task(UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = TextField(expand=1)

        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icon=icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)

    def delete_clicked(self, e):
        self.task_delete(self)

class TodoApp(UserControl):
    def build(self):
        self.new_task = TextField(hint_text="What needs to be done?", expand=True)
        self.tasks = Column()

        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="all"), Tab(text="active"), Tab(text="completed")],
        )

        return Column(
            controls=[
                Row(
                    controls=[
                        self.new_task,
                        FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked),
                    ],
                    alignment="center"
                ),
                Column(
                    controls=[
                        self.filter,
                        self.tasks,
                    ],
                    spacing=25
                )
            ],
            alignment="center",
            expand=True
        )

    def add_clicked(self, e):
        task = Task(self.new_task.value, self.task_status_change, self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def task_status_change(self, task):
        # TODO: Aquí deberías enviar una solicitud al backend para actualizar el estado de la tarea
        self.update()

    def task_delete(self, task):
        # TODO: Aquí deberías enviar una solicitud al backend para eliminar la tarea
        self.tasks.controls.remove(task)
        self.update()

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.tasks.controls:
            task.visible = (
                status == "all" or
                (status == "active" and not task.completed) or
                (status == "completed" and task.completed)
            )
        super().update()

    def tabs_changed(self, e):
        self.update()

class LoginPage(UserControl):
    def __init__(self, on_login_success, on_go_to_register):
        super().__init__()
        self.on_login_success = on_login_success
        self.on_go_to_register = on_go_to_register

    def build(self):
        self.username = TextField(label="Username", autofocus=True)
        self.password = TextField(label="Password", password=True)
        return Column(
            controls=[
                self.username,
                self.password,
                Row(
                    controls=[
                        FloatingActionButton(icon=icons.LOGIN, on_click=self.login_clicked, tooltip="Log in"),
                        FloatingActionButton(icon=icons.PERSON_ADD, on_click=lambda e: self.on_go_to_register(), tooltip="Register")
                    ],
                    alignment="center"
                )
            ],
            alignment="center",
            expand=True
        )

    def login_clicked(self, e):
        username = self.username.value
        password = self.password.value
        data = json.dumps({"username": username, "password": password}).encode("utf-8")
        req = urllib.request.Request(f"{BACKEND_URL}/login", data=data, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                print("Respuesta del servidor al iniciar sesión:", result)  # Imprimir toda la respuesta
                if result.get('message') == 'Login successful':
                    # Si el mensaje es de éxito, proceder con el inicio de sesión
                    self.on_login_success()  # Llamar a esta función si el inicio de sesión es exitoso
                else:
                    # Si hay algún otro mensaje, considerarlo como un error de inicio de sesión
                    print("Error en el inicio de sesión.")
        except urllib.error.HTTPError as error:
            print(f"Error al iniciar sesión: {error.read().decode()}")
        except urllib.error.URLError as error:
            print(f"Error de URL: {error.reason}")

class RegisterPage(UserControl):
    def __init__(self, on_go_to_login):
        super().__init__()
        self.on_go_to_login = on_go_to_login

    def build(self):
        self.username = TextField(label="Username")
        self.password = TextField(label="Password", password=True)
        self.confirm_password = TextField(label="Confirm Password", password=True)

        return Column(
            controls=[
                self.username,
                self.password,
                self.confirm_password,
                Row(
                    controls=[
                        FloatingActionButton(icon=icons.CHECK, on_click=self.register_clicked, tooltip="Register"),
                        FloatingActionButton(icon=icons.ARROW_BACK, on_click=lambda e: self.on_go_to_login(), tooltip="Back to Login")
                    ],
                    alignment="center"
                )
            ],
            alignment="center",
            expand=True
        )

    def register_clicked(self, e):
        username = self.username.value
        password = self.password.value
        confirm_password = self.confirm_password.value
        if password != confirm_password:
            print("Passwords do not match.")
            return
        data = json.dumps({"username": username, "password": password}).encode("utf-8")
        req = urllib.request.Request(f"{BACKEND_URL}/register", data=data, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                print("Respuesta del servidor al registrar:", result)  # Imprimir toda la respuesta
                self.on_go_to_login()  # Regresar a la página de inicio de sesión si el registro es exitoso
        except urllib.error.HTTPError as error:
            print(f"Error al registrar: {error.read().decode()}")
        except urllib.error.URLError as error:
            print(f"Error de URL: {error.reason}")

def main(page: Page):
    def show_login():
        page.controls.clear()
        login_page = LoginPage(on_login_success=show_app, on_go_to_register=show_register)
        page.add(login_page)

    def show_register():
        page.controls.clear()
        register_page = RegisterPage(on_go_to_login=show_login)
        page.add(register_page)

    def show_app():
        page.controls.clear()
        todo_app = TodoApp()
        page.add(todo_app)

    show_login()

flet.app(target=main)