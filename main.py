from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex, platform

from encuestas import supabase, obtener_todas_las_encuestas

# ==========================================
# VENTANA: tamaño cómodo en PC, normal en Android
# ==========================================
if platform in ("win", "linux", "macosx"):
    Window.size = (1000, 700)
    Window.minimum_width = 700
    Window.minimum_height = 500
elif platform == "android":
    # Que el teclado no tape el campo que se está escribiendo
    Window.softinput_mode = "below_target"

# Fondo claro (los textos oscuros se leen bien)
Window.clearcolor = get_color_from_hex("#f1f5f9")

# Rol que ve todas las encuestas; los demás solo las que tienen asignadas
ROLES_ACCESO_TOTAL = ('central',)


def crear_label(texto, **kw):
    """Label alineado a la izquierda, con salto de línea y altura automática."""
    lbl = Label(text=texto, size_hint_y=None, halign='left', valign='middle', **kw)
    lbl.bind(width=lambda i, w: setattr(i, 'text_size', (w, None)))
    lbl.bind(texture_size=lambda i, ts: setattr(i, 'height', ts[1] + dp(10)))
    return lbl


class AppMovilKivy(App):
    def build(self):
        self.title = "VotaFácil Mobile"
        self.usuario_actual = None
        self.respuestas_entradas = {}
        self.preguntas_actuales = []
        self.mapa_encuestas = {}

        self.root_layout = BoxLayout(orientation='vertical')
        self.mostrar_login()
        return self.root_layout

    def limpiar_pantalla(self):
        self.root_layout.clear_widgets()

    # ==========================================
    # PANTALLA DE LOGIN
    # ==========================================
    def mostrar_login(self):
        self.limpiar_pantalla()

        # Contenedor que centra el formulario (en PC no se estira a todo el ancho)
        centrado = AnchorLayout(anchor_x='center', anchor_y='center')

        login_layout = BoxLayout(
            orientation='vertical', padding=30, spacing=15,
            size_hint=(1, None), height=dp(470),
            size_hint_max_x=dp(420)
        )

        # Título
        login_layout.add_widget(Label(
            text="VotaFácil",
            font_size='28sp',
            bold=True,
            color=get_color_from_hex("#4f46e5"),
            size_hint_y=None, height=40
        ))
        login_layout.add_widget(Label(
            text="Módulo de Campo",
            font_size='14sp',
            color=get_color_from_hex("#64748b"),
            size_hint_y=None, height=30
        ))

        # Campo Usuario
        login_layout.add_widget(crear_label(
            "Nombre de Usuario:",
            font_size='14sp',
            color=get_color_from_hex("#1e293b")
        ))
        self.input_usuario = TextInput(multiline=False, size_hint_y=None, height=40)
        login_layout.add_widget(self.input_usuario)

        # Campo Contraseña
        login_layout.add_widget(crear_label(
            "Contraseña:",
            font_size='14sp',
            color=get_color_from_hex("#1e293b")
        ))
        self.input_pass = TextInput(password=True, multiline=False, size_hint_y=None, height=40)
        login_layout.add_widget(self.input_pass)

        # Mensaje de estado/error
        self.lbl_error = Label(text="", color=(1, 0, 0, 1), size_hint_y=None, height=30)
        login_layout.add_widget(self.lbl_error)

        # Botón Ingresar
        btn_login = Button(
            text="Iniciar Sesión",
            background_color=get_color_from_hex("#4f46e5"),
            color=(1, 1, 1, 1),
            size_hint_y=None, height=50,
            bold=True
        )
        btn_login.bind(on_press=self.verificar_login)
        login_layout.add_widget(btn_login)

        centrado.add_widget(login_layout)
        self.root_layout.add_widget(centrado)

    def verificar_login(self, instance):
        nombre = self.input_usuario.text.strip()
        password = self.input_pass.text.strip()

        if not nombre or not password:
            self.lbl_error.text = "Ingresa usuario y contraseña"
            return

        try:
            res = supabase.table("usuarios").select("*").eq("nombre", nombre).eq("password", password).execute()
            if res.data:
                self.usuario_actual = res.data[0]
                self.cargar_pantalla_principal()
            else:
                self.lbl_error.text = "Usuario o contraseña incorrectos"
        except Exception as e:
            self.lbl_error.text = f"Error de conexión: {e}"

    # ==========================================
    # PANTALLA PRINCIPAL
    # ==========================================
    def cargar_pantalla_principal(self):
        self.limpiar_pantalla()

        # Barra Superior (con fondo propio)
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)
        with top_bar.canvas.before:
            Color(*get_color_from_hex("#4f46e5"))
            rect = Rectangle(pos=top_bar.pos, size=top_bar.size)
        top_bar.bind(
            pos=lambda i, v: setattr(rect, 'pos', v),
            size=lambda i, v: setattr(rect, 'size', v)
        )

        top_bar.add_widget(Label(
            text=f"{self.usuario_actual['nombre']}",
            font_size='14sp', bold=True,
            color=(1, 1, 1, 1)
        ))
        btn_salir = Button(
            text="Salir",
            background_color=get_color_from_hex("#ef4444"),
            color=(1, 1, 1, 1),
            size_hint_x=None, width=70
        )
        btn_salir.bind(on_press=lambda x: self.mostrar_login())
        top_bar.add_widget(btn_salir)
        self.root_layout.add_widget(top_bar)

        # Selector de Encuestas
        self.spinner_encuestas = Spinner(
            text='Seleccionar Encuesta',
            values=(),
            size_hint_y=None, height=45,
            background_color=get_color_from_hex("#0d9488"),
            color=(1, 1, 1, 1)
        )
        self.spinner_encuestas.bind(text=self.cargar_preguntas)
        self.root_layout.add_widget(self.spinner_encuestas)

        # Contenedor Desplazable para Preguntas
        self.scroll = ScrollView(size_hint=(1, 1))
        self.box_preguntas = GridLayout(cols=1, spacing=15, padding=15, size_hint_y=None)
        self.box_preguntas.bind(minimum_height=self.box_preguntas.setter('height'))
        self.scroll.add_widget(self.box_preguntas)

        self.root_layout.add_widget(self.scroll)

        # Mensaje de estado inferior
        self.lbl_status = Label(text="", size_hint_y=None, height=30, color=(0, 0.6, 0, 1))
        self.root_layout.add_widget(self.lbl_status)

        self.poblar_encuestas()

    def poblar_encuestas(self):
        try:
            if self.usuario_actual['rol'] in ROLES_ACCESO_TOTAL:
                encuestas = obtener_todas_las_encuestas()
            else:
                permisos = supabase.table("permisos_encuestas").select("encuesta_id").eq("usuario_id", self.usuario_actual['id']).execute()
                ids = [p['encuesta_id'] for p in permisos.data]
                encuestas = supabase.table("encuestas").select("*").in_("id", ids).execute().data if ids else []

            self.mapa_encuestas = {e['titulo']: e['id'] for e in encuestas}
            self.spinner_encuestas.values = tuple(self.mapa_encuestas.keys())

            if not self.mapa_encuestas:
                self.lbl_status.color = (0.8, 0.4, 0, 1)
                self.lbl_status.text = "No hay encuestas disponibles para este usuario"
        except Exception as e:
            print(f"Error cargando encuestas: {e}")
            self.lbl_status.color = (1, 0, 0, 1)
            self.lbl_status.text = f"Error cargando encuestas: {e}"

    def cargar_preguntas(self, spinner, text):
        if text not in self.mapa_encuestas:
            return

        encuesta_id = self.mapa_encuestas[text]
        self.box_preguntas.clear_widgets()
        self.respuestas_entradas.clear()
        self.lbl_status.text = ""

        try:
            res = supabase.table("preguntas").select("*").eq("encuesta_id", encuesta_id).order("orden").execute()
            self.preguntas_actuales = res.data

            for idx, p in enumerate(self.preguntas_actuales, start=1):
                # Encabezado pregunta (con salto de línea y altura automática)
                self.box_preguntas.add_widget(crear_label(
                    f"{idx}. {p['texto_pregunta']}",
                    font_size='14sp', bold=True,
                    color=get_color_from_hex("#1e293b")
                ))

                if p['tipo_pregunta'] == 'opcion_unica':
                    op_res = supabase.table("opciones").select("*").eq("pregunta_id", p['id']).order("orden").execute()
                    box_opciones = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
                    box_opciones.bind(minimum_height=box_opciones.setter('height'))

                    # Guardaremos la opción seleccionada
                    opcion_seleccionada = {'val': ''}

                    def update_op(instance, value, val_text=opcion_seleccionada):
                        # ToggleButton usa "state" ('down' / 'normal'), no "active"
                        if value == 'down':
                            val_text['val'] = instance.text
                        elif val_text['val'] == instance.text:
                            val_text['val'] = ''

                    for op in op_res.data:
                        btn_op = ToggleButton(
                            text=op['texto_opcion'],
                            group=f"preg_{p['id']}",
                            size_hint_y=None, height=40
                        )
                        btn_op.bind(state=update_op)
                        box_opciones.add_widget(btn_op)

                    self.box_preguntas.add_widget(box_opciones)
                    self.respuestas_entradas[p['id']] = opcion_seleccionada
                else:
                    input_texto = TextInput(multiline=False, size_hint_y=None, height=40)
                    self.box_preguntas.add_widget(input_texto)
                    self.respuestas_entradas[p['id']] = input_texto

            # Botón de Enviar Respuestas al final
            btn_enviar = Button(
                text="Enviar Respuestas",
                background_color=get_color_from_hex("#4f46e5"),
                color=(1, 1, 1, 1),
                size_hint_y=None, height=50, bold=True
            )
            btn_enviar.bind(on_press=self.guardar_respuestas)
            self.box_preguntas.add_widget(btn_enviar)

        except Exception as e:
            self.lbl_status.color = (1, 0, 0, 1)
            self.lbl_status.text = f"Error cargando preguntas: {e}"

    def guardar_respuestas(self, instance):
        try:
            guardadas = 0
            for preg_id, item in self.respuestas_entradas.items():
                if isinstance(item, dict):
                    val = item['val']
                else:
                    val = item.text.strip()

                if val:
                    supabase.table("respuestas").insert({
                        "pregunta_id": preg_id,
                        "usuario_id": self.usuario_actual['id'],
                        "respuesta_texto": val
                    }).execute()
                    guardadas += 1

            if guardadas > 0:
                self.lbl_status.color = (0, 0.6, 0, 1)
                self.lbl_status.text = f"¡{guardadas} respuestas subidas con éxito!"
                self.box_preguntas.clear_widgets()
            else:
                self.lbl_status.color = (0.8, 0.4, 0, 1)
                self.lbl_status.text = "Responde al menos una pregunta"
        except Exception as e:
            self.lbl_status.color = (1, 0, 0, 1)
            self.lbl_status.text = f"Error al subir: {e}"


if __name__ == '__main__':
    AppMovilKivy().run()