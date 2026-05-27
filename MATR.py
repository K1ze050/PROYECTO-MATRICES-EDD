import re
import os

class NodoMatriz:
    def __init__(self, fila, columna, color):
        self.fila = fila
        self.columna = columna
        self.color = color
        self.arriba = None
        self.abajo = None
        self.izquierda = None
        self.derecha = None

class NodoCabecera:
    def __init__(self, id_cabecera):
        self.id_cabecera = id_cabecera
        self.siguiente = None
        self.anterior = None
        self.acceso = None 

class ListaCabeceras:
    def __init__(self):
        self.primero = None

    def insertar_ordenado(self, nuevo_nodo):
        if not self.primero:
            self.primero = nuevo_nodo
        elif nuevo_nodo.id_cabecera < self.primero.id_cabecera:
            nuevo_nodo.siguiente = self.primero
            self.primero.anterior = nuevo_nodo
            self.primero = nuevo_nodo
        else:
            actual = self.primero
            while actual.siguiente and actual.siguiente.id_cabecera < nuevo_nodo.id_cabecera:
                actual = actual.siguiente
            nuevo_nodo.siguiente = actual.siguiente
            if actual.siguiente:
                actual.siguiente.anterior = nuevo_nodo
            nuevo_nodo.anterior = actual
            actual.siguiente = nuevo_nodo

    def buscar(self, id_cabecera):
        actual = self.primero
        while actual:
            if actual.id_cabecera == id_cabecera:
                return actual
            actual = actual.siguiente
        return None

class NodoCapaABB:
    def __init__(self, id_capa):
        self.id_capa = id_capa
        self.matriz = MatrizDispersa() 
        self.izquierdo = None
        self.derecho = None

class NodoCapaImagen:
    def __init__(self, capa_ref):
        self.capa_ref = capa_ref
        self.siguiente = None

class NodoImagen:
    def __init__(self, id_imagen):
        self.id_imagen = id_imagen
        self.capas_head = None
        self.siguiente = None
        self.anterior = None

    def agregar_capa(self, capa_ref):
        nuevo = NodoCapaImagen(capa_ref)
        if not self.capas_head:
            self.capas_head = nuevo
        else:
            actual = self.capas_head
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

class NodoImagenUsuario:
    def __init__(self, id_imagen):
        self.id_imagen = id_imagen 
        self.siguiente = None

class NodoUsuarioABB:
    def __init__(self, nombre_usuario):
        self.nombre_usuario = nombre_usuario
        self.imagenes_head = None
        self.izquierdo = None
        self.derecho = None
        
    def agregar_imagen(self, id_imagen):
        nuevo = NodoImagenUsuario(id_imagen)
        if not self.imagenes_head:
            self.imagenes_head = nuevo
        else:
            actual = self.imagenes_head
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

class MatrizDispersa:
    def __init__(self):
        self.filas = ListaCabeceras()
        self.columnas = ListaCabeceras()

    def insertar(self, fila, columna, color):
        nuevo_nodo = NodoMatriz(fila, columna, color)
        nodo_fila = self.filas.buscar(fila)
        if not nodo_fila:
            nodo_fila = NodoCabecera(fila)
            self.filas.insertar_ordenado(nodo_fila)
            
        nodo_columna = self.columnas.buscar(columna)
        if not nodo_columna:
            nodo_columna = NodoCabecera(columna)
            self.columnas.insertar_ordenado(nodo_columna)
            
        if not nodo_fila.acceso:
            nodo_fila.acceso = nuevo_nodo
        elif nuevo_nodo.columna < nodo_fila.acceso.columna:
            nuevo_nodo.derecha = nodo_fila.acceso
            nodo_fila.acceso.izquierda = nuevo_nodo
            nodo_fila.acceso = nuevo_nodo
        else:
            actual = nodo_fila.acceso
            while actual.derecha and actual.derecha.columna < nuevo_nodo.columna:
                actual = actual.derecha
            nuevo_nodo.derecha = actual.derecha
            if actual.derecha:
                actual.derecha.izquierda = nuevo_nodo
            nuevo_nodo.izquierda = actual
            actual.derecha = nuevo_nodo

        if not nodo_columna.acceso:
            nodo_columna.acceso = nuevo_nodo
        elif nuevo_nodo.fila < nodo_columna.acceso.fila:
            nuevo_nodo.abajo = nodo_columna.acceso
            nodo_columna.acceso.arriba = nuevo_nodo
            nodo_columna.acceso = nuevo_nodo
        else:
            actual = nodo_columna.acceso
            while actual.abajo and actual.abajo.fila < nuevo_nodo.fila:
                actual = actual.abajo
            nuevo_nodo.abajo = actual.abajo
            if actual.abajo:
                actual.abajo.arriba = nuevo_nodo
            nuevo_nodo.arriba = actual
            actual.abajo = nuevo_nodo

    def obtener_pixeles(self):
        pixeles = []
        fila_actual = self.filas.primero
        while fila_actual:
            nodo_actual = fila_actual.acceso
            while nodo_actual:
                pixeles.append((nodo_actual.fila, nodo_actual.columna, nodo_actual.color))
                nodo_actual = nodo_actual.derecha
            fila_actual = fila_actual.siguiente
        return pixeles

class ArbolCapas:
    def __init__(self):
        self.raiz = None

    def insertar(self, id_capa):
        self.raiz = self._insertar_recursivo(self.raiz, id_capa)

    def _insertar_recursivo(self, actual, id_capa):
        if actual is None:
            return NodoCapaABB(id_capa)
        if id_capa < actual.id_capa:
            actual.izquierdo = self._insertar_recursivo(actual.izquierdo, id_capa)
        elif id_capa > actual.id_capa:
            actual.derecho = self._insertar_recursivo(actual.derecho, id_capa)
        return actual

    def buscar(self, id_capa):
        return self._buscar_recursivo(self.raiz, id_capa)

    def _buscar_recursivo(self, actual, id_capa):
        if actual is None or actual.id_capa == id_capa:
            return actual
        if id_capa < actual.id_capa:
            return self._buscar_recursivo(actual.izquierdo, id_capa)
        return self._buscar_recursivo(actual.derecho, id_capa)

    def obtener_preorden(self, limite):
        resultado = []
        self._preorden(self.raiz, limite, resultado)
        return resultado

    def _preorden(self, nodo, limite, resultado):
        if nodo and len(resultado) < limite:
            resultado.append(nodo)
            self._preorden(nodo.izquierdo, limite, resultado)
            self._preorden(nodo.derecho, limite, resultado)

    def obtener_inorden(self, limite):
        resultado = []
        self._inorden(self.raiz, limite, resultado)
        return resultado

    def _inorden(self, nodo, limite, resultado):
        if nodo and len(resultado) < limite:
            self._inorden(nodo.izquierdo, limite, resultado)
            if len(resultado) < limite:
                resultado.append(nodo)
            self._inorden(nodo.derecho, limite, resultado)

    def obtener_postorden(self, limite):
        resultado = []
        self._postorden(self.raiz, limite, resultado)
        return resultado

    def _postorden(self, nodo, limite, resultado):
        if nodo and len(resultado) < limite:
            self._postorden(nodo.izquierdo, limite, resultado)
            self._postorden(nodo.derecho, limite, resultado)
            if len(resultado) < limite:
                resultado.append(nodo)

class ListaImagenes:
    def __init__(self):
        self.cabeza = None

    def insertar(self, id_imagen):
        nuevo = NodoImagen(id_imagen)
        if not self.cabeza:
            self.cabeza = nuevo
            self.cabeza.siguiente = self.cabeza
            self.cabeza.anterior = self.cabeza
        else:
            if id_imagen < self.cabeza.id_imagen:
                ultimo = self.cabeza.anterior
                nuevo.siguiente = self.cabeza
                nuevo.anterior = ultimo
                self.cabeza.anterior = nuevo
                ultimo.siguiente = nuevo
                self.cabeza = nuevo
            elif id_imagen == self.cabeza.id_imagen:
                return 
            else:
                actual = self.cabeza
                while actual.siguiente != self.cabeza and actual.siguiente.id_imagen < id_imagen:
                    actual = actual.siguiente
                if actual.id_imagen == id_imagen or (actual.siguiente != self.cabeza and actual.siguiente.id_imagen == id_imagen):
                    return 
                nuevo.siguiente = actual.siguiente
                nuevo.anterior = actual
                actual.siguiente.anterior = nuevo
                actual.siguiente = nuevo

    def buscar(self, id_imagen):
        if not self.cabeza: return None
        actual = self.cabeza
        while True:
            if actual.id_imagen == id_imagen:
                return actual
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return None

class ArbolUsuarios:
    def __init__(self):
        self.raiz = None

    def insertar(self, nombre_usuario):
        self.raiz = self._insertar_recursivo(self.raiz, nombre_usuario)

    def _insertar_recursivo(self, actual, nombre_usuario):
        if actual is None:
            return NodoUsuarioABB(nombre_usuario)
        if nombre_usuario < actual.nombre_usuario:
            actual.izquierdo = self._insertar_recursivo(actual.izquierdo, nombre_usuario)
        elif nombre_usuario > actual.nombre_usuario:
            actual.derecho = self._insertar_recursivo(actual.derecho, nombre_usuario)
        return actual

    def buscar(self, nombre_usuario):
        return self._buscar_recursivo(self.raiz, nombre_usuario)

    def _buscar_recursivo(self, actual, nombre_usuario):
        if actual is None or actual.nombre_usuario == nombre_usuario:
            return actual
        if nombre_usuario < actual.nombre_usuario:
            return self._buscar_recursivo(actual.izquierdo, nombre_usuario)
        return self._buscar_recursivo(actual.derecho, nombre_usuario)

class CargaMasiva:
    @staticmethod
    def cargar_capas(ruta_archivo, arbol_capas):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            bloques_capa = re.findall(r'(\d+)\s*\{([^}]*)\}', contenido)
            for id_str, datos in bloques_capa:
                id_capa = int(id_str)
                arbol_capas.insertar(id_capa)
                nodo_capa = arbol_capas.buscar(id_capa)
                pixeles = re.findall(r'(\d+)\s*,\s*(\d+)\s*,\s*(#[0-9a-fA-F]+)\s*;', datos)
                for fila_str, col_str, color in pixeles:
                    nodo_capa.matriz.insertar(int(fila_str), int(col_str), color.upper())
            print(f"Carga de capas completada exitosamente desde '{ruta_archivo}'.")
        except Exception as e:
            print(f"Error al cargar capas: {e}")

    @staticmethod
    def cargar_imagenes(ruta_archivo, lista_imagenes, arbol_capas):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            bloques_img = re.findall(r'(\d+)\s*\{([^}]*)\}', contenido)
            for id_str, capas_str in bloques_img:
                id_img = int(id_str)
                lista_imagenes.insertar(id_img)
                nodo_img = lista_imagenes.buscar(id_img)
                if capas_str.strip():
                    capas_ids = capas_str.split(',')
                    for cid_str in capas_ids:
                        if cid_str.strip():
                            cid = int(cid_str.strip())
                            capa_ref = arbol_capas.buscar(cid)
                            if capa_ref:
                                nodo_img.agregar_capa(capa_ref)
                            else:
                                print(f"Advertencia: Capa {cid} no existe.")
            print(f"Carga de imágenes completada exitosamente desde '{ruta_archivo}'.")
        except Exception as e:
            print(f"Error al cargar imágenes: {e}")

    @staticmethod
    def cargar_usuarios(ruta_archivo, arbol_usuarios):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            bloques_usr = re.findall(r'([a-zA-Z0-9_]+)\s*:\s*([^;]*)\s*;', contenido)
            for usr_nombre, imgs_str in bloques_usr:
                arbol_usuarios.insertar(usr_nombre)
                nodo_usr = arbol_usuarios.buscar(usr_nombre)
                if imgs_str.strip():
                    img_ids = imgs_str.split(',')
                    for img_id_str in img_ids:
                        if img_id_str.strip():
                            nodo_usr.agregar_imagen(int(img_id_str.strip()))
            print(f"Carga de usuarios completada exitosamente desde '{ruta_archivo}'.")
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")

class GeneradorImagenes:
    @staticmethod
    def _renderizar_html(lista_capas_nodos, nombre_salida):
        if not lista_capas_nodos:
            print("No hay capas para generar la imagen.")
            return

        mapa_pixeles = {}
        max_fila = 0
        max_col = 0

        for nodo_capa in lista_capas_nodos:
            pixeles = nodo_capa.matriz.obtener_pixeles()
            for fila, col, color in pixeles:
                mapa_pixeles[(fila, col)] = color
                if fila > max_fila: max_fila = fila
                if col > max_col: max_col = col

        if max_fila == 0 and max_col == 0:
            max_fila = 1
            max_col = 1
            mapa_pixeles[(1, 1)] = "#000000"

        html_content = "<html>\n<head><title>Imagen Generada</title></head>\n"
        html_content += "<body style='background-color: gray; display: flex; justify-content: center; align-items: center; height: 100vh;'>\n"
        html_content += "<table style='border-collapse: collapse;'>\n"

        for i in range(1, max_fila + 1):
            html_content += "  <tr>\n"
            for j in range(1, max_col + 1):
                color = mapa_pixeles.get((i, j), "#FFFFFF")
                html_content += f"    <td style='width: 20px; height: 20px; background-color: {color};'></td>\n"
            html_content += "  </tr>\n"
        
        html_content += "</table>\n</body>\n</html>"

        os.makedirs("imagenes_generadas", exist_ok=True)
        ruta = f"imagenes_generadas/{nombre_salida}.html"
        with open(ruta, "w", encoding='utf-8') as f:
            f.write(html_content)
        print(f"Imagen '{nombre_salida}' generada exitosamente.")

    @classmethod
    def por_recorrido_limitado(cls, arbol_capas, tipo, limite):
        capas = []
        if tipo.lower() == "preorden":
            capas = arbol_capas.obtener_preorden(limite)
        elif tipo.lower() == "inorden":
            capas = arbol_capas.obtener_inorden(limite)
        elif tipo.lower() == "postorden":
            capas = arbol_capas.obtener_postorden(limite)
        else:
            print("Tipo de recorrido no válido.")
            return
        
        cls._renderizar_html(capas, f"recorrido_{tipo}_{limite}")

    @classmethod
    def por_lista_imagenes(cls, lista_imagenes, id_imagen):
        nodo_img = lista_imagenes.buscar(id_imagen)
        if not nodo_img:
            print(f"La imagen {id_imagen} no existe.")
            return

        capas = []
        actual = nodo_img.capas_head
        while actual:
            capas.append(actual.capa_ref)
            actual = actual.siguiente
        
        cls._renderizar_html(capas, f"imagen_{id_imagen}")

    @classmethod
    def por_capa(cls, arbol_capas, id_capa):
        nodo_capa = arbol_capas.buscar(id_capa)
        if not nodo_capa:
            print(f"La capa {id_capa} no existe.")
            return
        cls._renderizar_html([nodo_capa], f"capa_{id_capa}")

    @classmethod
    def por_usuario(cls, arbol_usuarios, lista_imagenes, nombre_usuario, id_imagen):
        nodo_usr = arbol_usuarios.buscar(nombre_usuario)
        if not nodo_usr:
            print(f"El usuario '{nombre_usuario}' no existe.")
            return
        
        actual_img = nodo_usr.imagenes_head
        tiene_imagen = False
        while actual_img:
            if actual_img.id_imagen == id_imagen:
                tiene_imagen = True
                break
            actual_img = actual_img.siguiente
            
        if not tiene_imagen:
            print(f"El usuario '{nombre_usuario}' no tiene la imagen {id_imagen}.")
            return
            
        cls.por_lista_imagenes(lista_imagenes, id_imagen)