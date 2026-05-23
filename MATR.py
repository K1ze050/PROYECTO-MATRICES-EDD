import re

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
                                print(f"Advertencia: Capa {cid} no existe. No se enlazó a la imagen {id_img}.")
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