from supabase import create_client, Client

SUPABASE_URL = "https://wwyldlwwtnbniniyvjjy.supabase.co"
SUPABASE_KEY = "sb_publishable_t6NEBEYDk2N0MS4sUlxlwg_mI0NQQNd"

# Cliente global exportado para app_pc.py
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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