import requests

SUPABASE_URL = "https://wwyldlwwtnbniniyvjjy.supabase.co"
SUPABASE_KEY = "sb_publishable_t6NEBEYDk2N0MS4sUlxlwg_mI0NQQNd"

TIMEOUT = 15  # segundos


# ==========================================
# CLIENTE MÍNIMO PARA LA API REST DE SUPABASE
# (reemplaza a la librería "supabase", que no compila en Android)
# Mantiene la misma forma de uso:
#   supabase.table("x").select("*").eq("a", 1).order("orden").execute().data
# ==========================================
class ErrorSupabase(Exception):
    pass


class RespuestaSupabase:
    def __init__(self, data):
        self.data = data


class Consulta:
    def __init__(self, cliente, tabla):
        self._cliente = cliente
        self._tabla = tabla
        self._metodo = "GET"
        self._columnas = "*"
        self._filtros = []
        self._cuerpo = None

    # ---- operaciones ----
    def select(self, columnas="*"):
        self._metodo = "GET"
        self._columnas = columnas
        return self

    def insert(self, datos):
        self._metodo = "POST"
        self._cuerpo = datos
        return self

    def update(self, datos):
        self._metodo = "PATCH"
        self._cuerpo = datos
        return self

    def delete(self):
        self._metodo = "DELETE"
        return self

    # ---- filtros ----
    def eq(self, columna, valor):
        self._filtros.append((columna, f"eq.{valor}"))
        return self

    def neq(self, columna, valor):
        self._filtros.append((columna, f"neq.{valor}"))
        return self

    def in_(self, columna, valores):
        lista = ",".join(str(v) for v in valores)
        self._filtros.append((columna, f"in.({lista})"))
        return self

    def order(self, columna, desc=False):
        self._filtros.append(("order", f"{columna}.{'desc' if desc else 'asc'}"))
        return self

    def limit(self, n):
        self._filtros.append(("limit", str(n)))
        return self

    # ---- ejecución ----
    def execute(self):
        url = f"{self._cliente.url}/rest/v1/{self._tabla}"
        headers = dict(self._cliente.headers)
        params = list(self._filtros)

        if self._metodo == "GET":
            params.insert(0, ("select", self._columnas))
        elif self._metodo == "DELETE":
            headers["Prefer"] = "return=minimal"
        else:
            # insert / update: devolver las filas afectadas (para leer el id)
            headers["Prefer"] = "return=representation"

        try:
            r = requests.request(
                self._metodo, url,
                params=params,
                json=self._cuerpo,
                headers=headers,
                timeout=TIMEOUT
            )
        except requests.RequestException as e:
            raise ErrorSupabase(f"Sin conexión: {e}")

        if r.status_code >= 400:
            raise ErrorSupabase(f"{r.status_code}: {r.text}")

        if not r.content:
            return RespuestaSupabase([])
        try:
            return RespuestaSupabase(r.json())
        except ValueError:
            return RespuestaSupabase([])


class Cliente:
    def __init__(self, url, key):
        self.url = url.rstrip("/")
        self.headers = {
            "apikey": key,
            "Content-Type": "application/json",
        }
        # Las llaves antiguas (JWT, empiezan con "eyJ") también van en Authorization.
        # Las nuevas "sb_publishable_..." solo usan el header apikey.
        if key.startswith("eyJ"):
            self.headers["Authorization"] = f"Bearer {key}"

    def table(self, nombre):
        return Consulta(self, nombre)


# Cliente global exportado para la app
supabase = Cliente(SUPABASE_URL, SUPABASE_KEY)


# ==========================================
# FUNCIONES (sin cambios)
# ==========================================
def crear_encuesta(titulo, descripcion):
    """Crea una nueva encuesta en la nube y devuelve su ID"""
    try:
        response = supabase.table("encuestas").insert({
            "titulo": titulo,
            "descripcion": descripcion,
            "estado": 1
        }).execute()

        encuesta_id = response.data[0]['id']
        return encuesta_id
    except Exception as e:
        print(f"Error al crear encuesta: {e}")
        return None


def agregar_pregunta(encuesta_id, texto_pregunta, tipo_pregunta, orden=0):
    """Agrega una pregunta asociada a una encuesta específica"""
    try:
        response = supabase.table("preguntas").insert({
            "encuesta_id": encuesta_id,
            "texto_pregunta": texto_pregunta,
            "tipo_pregunta": tipo_pregunta,
            "orden": orden
        }).execute()

        pregunta_id = response.data[0]['id']
        return pregunta_id
    except Exception as e:
        print(f"Error al agregar pregunta: {e}")
        return None


def agregar_opcion(pregunta_id, texto_opcion, orden=0):
    """Agrega una opción de respuesta para preguntas de selección"""
    try:
        supabase.table("opciones").insert({
            "pregunta_id": pregunta_id,
            "texto_opcion": texto_opcion,
            "orden": orden
        }).execute()
    except Exception as e:
        print(f"Error al agregar opción: {e}")


def obtener_todas_las_encuestas():
    """Consulta todas las encuestas almacenadas en la nube"""
    try:
        response = supabase.table("encuestas").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al consultar encuestas: {e}")
        return []


def obtener_resumen_respuestas(encuesta_id):
    """Obtiene el conteo total de respuestas agrupadas por pregunta y opción"""
    try:
        preguntas_resp = supabase.table("preguntas").select("*").eq("encuesta_id", encuesta_id).execute()
        preguntas = preguntas_resp.data

        resumen = []
        for preg in preguntas:
            if preg['tipo_pregunta'] == 'opcion_unica':
                opciones_resp = supabase.table("opciones").select("*").eq("pregunta_id", preg['id']).execute()
                opciones = opciones_resp.data

                respuestas_resp = supabase.table("respuestas").select("*").eq("pregunta_id", preg['id']).execute()
                respuestas = respuestas_resp.data

                conteo = {op['texto_opcion']: 0 for op in opciones}
                for r in respuestas:
                    texto = r['respuesta_texto']
                    if texto in conteo:
                        conteo[texto] += 1
                    else:
                        conteo[texto] = conteo.get(texto, 0) + 1

                resumen.append({
                    "pregunta": preg['texto_pregunta'],
                    "conteo": conteo
                })
        return resumen
    except Exception as e:
        print(f"Error al obtener resumen de respuestas: {e}")
        return []


def actualizar_usuario(usuario_id, nuevo_nombre, nueva_password, nuevo_rol):
    """Actualiza los datos de un usuario existente"""
    try:
        supabase.table("usuarios").update({
            "nombre": nuevo_nombre,
            "password": nueva_password,
            "rol": nuevo_rol
        }).eq("id", usuario_id).execute()
        return True
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return False


def eliminar_usuario(usuario_id):
    """Elimina un usuario del sistema"""
    try:
        supabase.table("usuarios").delete().eq("id", usuario_id).execute()
        return True
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False


def eliminar_encuesta(encuesta_id):
    """Elimina una encuesta completa"""
    try:
        supabase.table("encuestas").delete().eq("id", encuesta_id).execute()
        return True
    except Exception as e:
        print(f"Error al eliminar encuesta: {e}")
        return False


def eliminar_opcion(opcion_id):
    """Elimina una opción de respuesta específica"""
    try:
        supabase.table("opciones").delete().eq("id", opcion_id).execute()
        return True
    except Exception as e:
        print(f"Error al eliminar opción: {e}")
        return False