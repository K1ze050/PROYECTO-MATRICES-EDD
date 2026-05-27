import re
import os

class NdMat:
    def __init__(self, f, c, col):
        self.f = f; self.c = c; self.col = col
        self.up = None; self.dw = None; self.lf = None; self.rg = None

class NdCab:
    def __init__(self, id_cb):
        self.id_cb = id_cb; self.nxt = None; self.prv = None; self.acc = None 

class LstCab:
    def __init__(self): self.prm = None
    
    def ins_ord(self, n_nd):
        if not self.prm: self.prm = n_nd
        elif n_nd.id_cb < self.prm.id_cb:
            n_nd.nxt = self.prm; self.prm.prv = n_nd; self.prm = n_nd
        else:
            act = self.prm
            while act.nxt and act.nxt.id_cb < n_nd.id_cb: act = act.nxt
            n_nd.nxt = act.nxt
            if act.nxt: act.nxt.prv = n_nd
            n_nd.prv = act; act.nxt = n_nd
            
    def bsc(self, id_cb):
        act = self.prm
        while act:
            if act.id_cb == id_cb: return act
            act = act.nxt
        return None

class NdCpABB:
    def __init__(self, id_cp):
        self.id_cp = id_cp; self.md = MatDisp(); self.izq = None; self.der = None

class NdCpImg:
    def __init__(self, cp_rf): self.cp_rf = cp_rf; self.nxt = None

class NdImg:
    def __init__(self, id_im):
        self.id_im = id_im; self.cps_hd = None; self.nxt = None; self.prv = None
        
    def add_cp(self, cp_rf):
        nvo = NdCpImg(cp_rf)
        if not self.cps_hd: self.cps_hd = nvo
        else:
            act = self.cps_hd
            while act.nxt: act = act.nxt
            act.nxt = nvo

class NdImgUsr:
    def __init__(self, id_im): self.id_im = id_im; self.nxt = None

class NdUsrABB:
    def __init__(self, nm_u):
        self.nm_u = nm_u; self.ims_hd = None; self.izq = None; self.der = None
        
    def add_im(self, id_im):
        nvo = NdImgUsr(id_im)
        if not self.ims_hd: self.ims_hd = nvo
        else:
            act = self.ims_hd
            while act.nxt: act = act.nxt
            act.nxt = nvo
            
    def del_im(self, id_im):
        if not self.ims_hd: return False
        if self.ims_hd.id_im == id_im: self.ims_hd = self.ims_hd.nxt; return True
        act = self.ims_hd
        while act.nxt:
            if act.nxt.id_im == id_im: act.nxt = act.nxt.nxt; return True
            act = act.nxt
        return False

class MatDisp:
    def __init__(self): self.fls = LstCab(); self.cls = LstCab()
    
    def ins(self, f, c, col):
        nvo = NdMat(f, c, col)
        nd_f = self.fls.bsc(f)
        if not nd_f: nd_f = NdCab(f); self.fls.ins_ord(nd_f)
        nd_c = self.cls.bsc(c)
        if not nd_c: nd_c = NdCab(c); self.cls.ins_ord(nd_c)
        
        if not nd_f.acc: nd_f.acc = nvo
        elif nvo.c < nd_f.acc.c:
            nvo.rg = nd_f.acc; nd_f.acc.lf = nvo; nd_f.acc = nvo
        else:
            act = nd_f.acc
            while act.rg and act.rg.c < nvo.c: act = act.rg
            nvo.rg = act.rg
            if act.rg: act.rg.lf = nvo
            nvo.lf = act; act.rg = nvo
            
        if not nd_c.acc: nd_c.acc = nvo
        elif nvo.f < nd_c.acc.f:
            nvo.dw = nd_c.acc; nd_c.acc.up = nvo; nd_c.acc = nvo
        else:
            act = nd_c.acc
            while act.dw and act.dw.f < nvo.f: act = act.dw
            nvo.dw = act.dw
            if act.dw: act.dw.up = nvo
            nvo.up = act; act.dw = nvo
            
    def obt_px(self):
        pxs = []; f_act = self.fls.prm
        while f_act:
            n_act = f_act.acc
            while n_act: pxs.append((n_act.f, n_act.c, n_act.col)); n_act = n_act.rg
            f_act = f_act.nxt
        return pxs

class AbbCps:
    def __init__(self): self.rz = None
    
    def ins(self, id_cp): self.rz = self._ins_rec(self.rz, id_cp)
    def _ins_rec(self, act, id_cp):
        if act is None: return NdCpABB(id_cp)
        if id_cp < act.id_cp: act.izq = self._ins_rec(act.izq, id_cp)
        elif id_cp > act.id_cp: act.der = self._ins_rec(act.der, id_cp)
        return act
        
    def bsc(self, id_cp): return self._bsc_rec(self.rz, id_cp)
    def _bsc_rec(self, act, id_cp):
        if act is None or act.id_cp == id_cp: return act
        if id_cp < act.id_cp: return self._bsc_rec(act.izq, id_cp)
        return self._bsc_rec(act.der, id_cp)
        
    def obt_pre(self, lm): res = []; self._pre(self.rz, lm, res); return res
    def _pre(self, nd, lm, res):
        if nd and len(res) < lm: res.append(nd); self._pre(nd.izq, lm, res); self._pre(nd.der, lm, res)
        
    def obt_in(self, lm): res = []; self._in(self.rz, lm, res); return res
    def _in(self, nd, lm, res):
        if nd and len(res) < lm:
            self._in(nd.izq, lm, res)
            if len(res) < lm: res.append(nd)
            self._in(nd.der, lm, res)
            
    def obt_pos(self, lm): res = []; self._pos(self.rz, lm, res); return res
    def _pos(self, nd, lm, res):
        if nd and len(res) < lm:
            self._pos(nd.izq, lm, res); self._pos(nd.der, lm, res)
            if len(res) < lm: res.append(nd)

class LstImgs:
    def __init__(self): self.cbz = None
    
    def ins(self, id_im):
        nvo = NdImg(id_im)
        if not self.cbz: self.cbz = nvo; self.cbz.nxt = self.cbz; self.cbz.prv = self.cbz
        else:
            if id_im < self.cbz.id_im:
                ult = self.cbz.prv; nvo.nxt = self.cbz; nvo.prv = ult
                self.cbz.prv = nvo; ult.nxt = nvo; self.cbz = nvo
            elif id_im == self.cbz.id_im: return 
            else:
                act = self.cbz
                while act.nxt != self.cbz and act.nxt.id_im < id_im: act = act.nxt
                if act.id_im == id_im or (act.nxt != self.cbz and act.nxt.id_im == id_im): return 
                nvo.nxt = act.nxt; nvo.prv = act; act.nxt.prv = nvo; act.nxt = nvo
                
    def bsc(self, id_im):
        if not self.cbz: return None
        act = self.cbz
        while True:
            if act.id_im == id_im: return act
            act = act.nxt
            if act == self.cbz: break
        return None
        
    def rmv(self, id_im):
        if not self.cbz: return False
        act = self.cbz
        while True:
            if act.id_im == id_im:
                if act.nxt == self.cbz and act.prv == self.cbz: self.cbz = None
                else:
                    act.prv.nxt = act.nxt; act.nxt.prv = act.prv
                    if act == self.cbz: self.cbz = act.nxt
                return True
            act = act.nxt
            if act == self.cbz: break
        return False

class AbbUsrs:
    def __init__(self): self.rz = None
    
    def ins(self, nm_u): self.rz = self._ins_rec(self.rz, nm_u)
    def _ins_rec(self, act, nm_u):
        if act is None: return NdUsrABB(nm_u)
        if nm_u < act.nm_u: act.izq = self._ins_rec(act.izq, nm_u)
        elif nm_u > act.nm_u: act.der = self._ins_rec(act.der, nm_u)
        return act
        
    def bsc(self, nm_u): return self._bsc_rec(self.rz, nm_u)
    def _bsc_rec(self, act, nm_u):
        if act is None or act.nm_u == nm_u: return act
        if nm_u < act.nm_u: return self._bsc_rec(act.izq, nm_u)
        return self._bsc_rec(act.der, nm_u)
        
    def rmv(self, nm_u): self.rz = self._rmv_rec(self.rz, nm_u)
    def _rmv_rec(self, act, nm_u):
        if act is None: return act
        if nm_u < act.nm_u: act.izq = self._rmv_rec(act.izq, nm_u)
        elif nm_u > act.nm_u: act.der = self._rmv_rec(act.der, nm_u)
        else:
            if act.izq is None: return act.der
            elif act.der is None: return act.izq
            tmp = self._min_nd(act.der)
            act.nm_u = tmp.nm_u; act.ims_hd = tmp.ims_hd
            act.der = self._rmv_rec(act.der, tmp.nm_u)
        return act
        
    def _min_nd(self, nd):
        act = nd
        while act.izq is not None: act = act.izq
        return act

class CgMas:
    @staticmethod
    def ld_cps(rt_arch, ab_c):
        try:
            with open(rt_arch, 'r', encoding='utf-8') as f: cnt = f.read()
            blqs = re.findall(r'(\d+)\s*\{([^}]*)\}', cnt)
            for id_s, dts in blqs:
                i_cp = int(id_s); ab_c.ins(i_cp); nd_cp = ab_c.bsc(i_cp)
                pxs = re.findall(r'(\d+)\s*,\s*(\d+)\s*,\s*(#[0-9a-fA-F]+)\s*;', dts)
                for f_s, c_s, cl in pxs: nd_cp.md.ins(int(f_s), int(c_s), cl.upper())
        except Exception: pass
        
    @staticmethod
    def ld_ims(rt_arch, ls_i, ab_c):
        try:
            with open(rt_arch, 'r', encoding='utf-8') as f: cnt = f.read()
            blqs = re.findall(r'(\d+)\s*\{([^}]*)\}', cnt)
            for id_s, cps_s in blqs:
                i_im = int(id_s); ls_i.ins(i_im); nd_im = ls_i.bsc(i_im)
                if cps_s.strip():
                    for id_c_s in cps_s.split(','):
                        if id_c_s.strip():
                            rf = ab_c.bsc(int(id_c_s.strip()))
                            if rf: nd_im.add_cp(rf)
        except Exception: pass
        
    @staticmethod
    def ld_usrs(rt_arch, ab_u):
        try:
            with open(rt_arch, 'r', encoding='utf-8') as f: cnt = f.read()
            blqs = re.findall(r'([a-zA-Z0-9_]+)\s*:\s*([^;]*)\s*;', cnt)
            for ur, ims_s in blqs:
                ab_u.ins(ur); nd_u = ab_u.bsc(ur)
                if ims_s.strip():
                    for id_i_s in ims_s.split(','):
                        if id_i_s.strip(): nd_u.add_im(int(id_i_s.strip()))
        except Exception: pass

class GenImg:
    @staticmethod
    def _rnd_ht(ls_nd, nm_out):
        if not ls_nd: return
        mp_px, mx_f, mx_c = {}, 0, 0
        for nd in ls_nd:
            for f, c, cl in nd.md.obt_px():
                mp_px[(f, c)] = cl; mx_f, mx_c = max(mx_f, f), max(mx_c, c)
        if mx_f == 0 and mx_c == 0: mx_f, mx_c = 1, 1; mp_px[(1, 1)] = "#000000"
        ht = "<html><body style='background-color: gray; display: flex; justify-content: center; align-items: center; height: 100vh;'><table style='border-collapse: collapse;'>"
        for i in range(1, mx_f + 1):
            ht += "<tr>"
            for j in range(1, mx_c + 1):
                cl = mp_px.get((i, j), "#FFFFFF")
                ht += f"<td style='width: 20px; height: 20px; background-color: {cl};'></td>"
            ht += "</tr>"
        ht += "</table></body></html>"
        os.makedirs("img_gen", exist_ok=True)
        with open(f"img_gen/{nm_out}.html", "w", encoding='utf-8') as f: f.write(ht)
        
    @classmethod
    def x_rec_lim(cls, ab_c, tp, lm):
        cps = []
        if tp.lower() == "preorden": cps = ab_c.obt_pre(lm)
        elif tp.lower() == "inorden": cps = ab_c.obt_in(lm)
        elif tp.lower() == "postorden": cps = ab_c.obt_pos(lm)
        else: return
        cls._rnd_ht(cps, f"rec_{tp}_{lm}")
        
    @classmethod
    def x_ls_im(cls, ls_im, i_im):
        nd_i = ls_im.bsc(i_im)
        if not nd_i: return
        cps, act = [], nd_i.cps_hd
        while act: cps.append(act.cp_rf); act = act.nxt
        cls._rnd_ht(cps, f"im_{i_im}")
        
    @classmethod
    def x_cp(cls, ab_c, i_cp):
        nd_c = ab_c.bsc(i_cp)
        if nd_c: cls._rnd_ht([nd_c], f"cp_{i_cp}")
        
    @classmethod
    def x_usr(cls, ab_u, ls_i, nm_u, i_im):
        nd_u = ab_u.bsc(nm_u)
        if not nd_u: return
        ac_im, tne = nd_u.ims_hd, False
        while ac_im:
            if ac_im.id_im == i_im: tne = True; break
            ac_im = ac_im.nxt
        if tne: cls.x_ls_im(ls_i, i_im)

class GtCRUD:
    @staticmethod
    def add_u(ab_u, nm_u):
        if not ab_u.bsc(nm_u): ab_u.ins(nm_u)
    @staticmethod
    def del_u(ab_u, nm_u):
        if ab_u.bsc(nm_u): ab_u.rmv(nm_u)
    @staticmethod
    def mod_u(ab_u, vj, nv):
        nd_v = ab_u.bsc(vj)
        if not nd_v or ab_u.bsc(nv): return
        ims = nd_v.ims_hd
        ab_u.rmv(vj); ab_u.ins(nv); ab_u.bsc(nv).ims_hd = ims
    @staticmethod
    def add_i(ls_i, ab_u, ab_c, nm_u, i_im, ids_c):
        nd_u = ab_u.bsc(nm_u)
        if not nd_u or ls_i.bsc(i_im): return
        ls_i.ins(i_im); nd_im = ls_i.bsc(i_im)
        for id_c in ids_c:
            rf = ab_c.bsc(id_c)
            if rf: nd_im.add_cp(rf)
        nd_u.add_im(i_im)
    @staticmethod
    def del_i(ls_i, ab_u, nm_u, i_im):
        nd_u = ab_u.bsc(nm_u)
        if nd_u and nd_u.del_im(i_im): ls_i.rmv(i_im)

class RepGvz:
    @staticmethod
    def _cmp_d(cd_d, nm_o):
        os.makedirs("reps", exist_ok=True)
        rt_d = f"reps/{nm_o}.dot"; rt_p = f"reps/{nm_o}.png"
        with open(rt_d, "w", encoding='utf-8') as f: f.write(cd_d)
        os.system(f"dot -Tpng {rt_d} -o {rt_p}")
        
    @classmethod
    def v_ls_i(cls, ls_i):
        if not ls_i.cbz: return
        dt = "digraph G {\n rankdir=LR;\n node [shape=box];\n"; ac = ls_i.cbz
        while True:
            dt += f' i_{ac.id_im} [label="Im: {ac.id_im}"];\n'
            dt += f' i_{ac.id_im} -> i_{ac.nxt.id_im};\n i_{ac.nxt.id_im} -> i_{ac.id_im};\n'
            if ac.cps_hd:
                a_c = ac.cps_hd
                dt += f' i_{ac.id_im} -> cp_{ac.id_im}_{id(a_c)} [dir=forward];\n'
                while a_c:
                    dt += f' cp_{ac.id_im}_{id(a_c)} [label="Cp: {a_c.cp_rf.id_cp}", shape=ellipse];\n'
                    if a_c.nxt: dt += f' cp_{ac.id_im}_{id(a_c)} -> cp_{ac.id_im}_{id(a_c.nxt)};\n'
                    a_c = a_c.nxt
            ac = ac.nxt
            if ac == ls_i.cbz: break
        dt += "}\n"; cls._cmp_d(dt, "lst_ims")
        
    @classmethod
    def v_ab_c(cls, ab_c):
        dt = "digraph G {\n node [shape=record];\n"
        def rc(nd):
            nonlocal dt
            if not nd: return
            dt += f' c_{nd.id_cp} [label="Cp: {nd.id_cp}"];\n'
            if nd.izq: dt += f' c_{nd.id_cp} -> c_{nd.izq.id_cp};\n'; rc(nd.izq)
            if nd.der: dt += f' c_{nd.id_cp} -> c_{nd.der.id_cp};\n'; rc(nd.der)
        rc(ab_c.rz); dt += "}\n"; cls._cmp_d(dt, "ab_cps")
        
    @classmethod
    def v_cp(cls, ab_c, i_c):
        nd = ab_c.bsc(i_c)
        if not nd: return
        dt = f'digraph G {{\n node [shape=box]; rankdir=TB;\n mtz [label="Cp {i_c}"];\n'
        f_a = nd.md.fls.prm
        while f_a:
            dt += f' F{f_a.id_cb} [label="{f_a.id_cb}", group=1];\n'
            if f_a == nd.md.fls.prm: dt += f' mtz -> F{f_a.id_cb};\n'
            if f_a.nxt: dt += f' F{f_a.id_cb} -> F{f_a.nxt.id_cb} [dir=both];\n'
            f_a = f_a.nxt
        c_a = nd.md.cls.prm
        dt += '{ rank=same; mtz; '
        while c_a: dt += f'C{c_a.id_cb}; '; c_a = c_a.nxt
        dt += '}\n'; c_a = nd.md.cls.prm
        while c_a:
            dt += f' C{c_a.id_cb} [label="{c_a.id_cb}", group={c_a.id_cb + 1}];\n'
            if c_a == nd.md.cls.prm: dt += f' mtz -> C{c_a.id_cb};\n'
            if c_a.nxt: dt += f' C{c_a.id_cb} -> C{c_a.nxt.id_cb} [dir=both];\n'
            c_a = c_a.nxt
        f_a = nd.md.fls.prm
        while f_a:
            n_a = f_a.acc; dt += f'{{ rank=same; F{f_a.id_cb}; '
            while n_a: dt += f'N_{n_a.f}_{n_a.c};  N_{n_a.f}_{n_a.c} [label="{n_a.col}", group={n_a.c + 1}];\n'; n_a = n_a.rg
            dt += '}\n'; n_a = f_a.acc; dt += f' F{f_a.id_cb} -> N_{n_a.f}_{n_a.c} [dir=both];\n'
            while n_a:
                if n_a.rg: dt += f' N_{n_a.f}_{n_a.c} -> N_{n_a.rg.f}_{n_a.rg.c} [dir=both];\n'
                n_a = n_a.rg
            f_a = f_a.nxt
        c_a = nd.md.cls.prm
        while c_a:
            n_a = c_a.acc; dt += f' C{c_a.id_cb} -> N_{n_a.f}_{n_a.c} [dir=both];\n'
            while n_a:
                if n_a.dw: dt += f' N_{n_a.f}_{n_a.c} -> N_{n_a.dw.f}_{n_a.dw.c} [dir=both];\n'
                n_a = n_a.dw
            c_a = c_a.nxt
        dt += "}\n"; cls._cmp_d(dt, f"mtz_cp_{i_c}")
        
    @classmethod
    def v_im_ab(cls, ab_c, ls_i, i_im):
        n_im = ls_i.bsc(i_im)
        if not n_im: return
        dt = f'digraph G {{\n rankdir=TB;\n node [shape=box];\n im [label="Im {i_im}", style=filled, fillcolor=lightcoral];\n'
        a_c = n_im.cps_hd
        if a_c:
            dt += f' im -> cl_{id(a_c)};\n'
            while a_c:
                dt += f' cl_{id(a_c)} [label="Rf Cp: {a_c.cp_rf.id_cp}", shape=ellipse, color=red];\n'
                dt += f' cl_{id(a_c)} -> ab_{a_c.cp_rf.id_cp} [color=red, constraint=false];\n'
                if a_c.nxt: dt += f' cl_{id(a_c)} -> cl_{id(a_c.nxt)};\n'
                a_c = a_c.nxt
        def rc(nd):
            nonlocal dt
            if not nd: return
            dt += f' ab_{nd.id_cp} [label="Cp: {nd.id_cp}"];\n'
            if nd.izq: dt += f' ab_{nd.id_cp} -> ab_{nd.izq.id_cp};\n'; rc(nd.izq)
            if nd.der: dt += f' ab_{nd.id_cp} -> ab_{nd.der.id_cp};\n'; rc(nd.der)
        rc(ab_c.rz); dt += "}\n"; cls._cmp_d(dt, f"ln_im_{i_im}")
        
    @classmethod
    def v_ab_u(cls, ab_u):
        dt = "digraph G {\n node [shape=record, color=blue];\n"
        def rc(nd):
            nonlocal dt
            if not nd: return
            dt += f' u_{nd.nm_u} [label="{nd.nm_u}"];\n'
            if nd.izq: dt += f' u_{nd.nm_u} -> u_{nd.izq.nm_u};\n'; rc(nd.izq)
            if nd.der: dt += f' u_{nd.nm_u} -> u_{nd.der.nm_u};\n'; rc(nd.der)
        rc(ab_u.rz); dt += "}\n"; cls._cmp_d(dt, "ab_usr")

def cnl_prnl():
    ab_c = AbbCps(); ls_i = LstImgs(); ab_u = AbbUsrs()
    while True:
        print("\n*** PANEL DE CONTROL PRINCIPAL ***")
        print("[1] Importación de Datos")
        print("[2] Renderizado Visual")
        print("[3] Administración de Registros")
        print("[4] Visualización de Memoria (Graphviz)")
        print("[5] Cerrar Sistema")
        op = input("Seleccione una opción: ")
        
        if op == "1":
            so = input("\n[1] Importar Capas\n[2] Importar Imágenes\n[3] Importar Usuarios\nSelección: ")
            rt = input("Ruta de origen: ")
            if so == "1": CgMas.ld_cps(rt, ab_c)
            elif so == "2": CgMas.ld_ims(rt, ls_i, ab_c)
            elif so == "3": CgMas.ld_usrs(rt, ab_u)
            
        elif op == "2":
            so = input("\n[1] Por método de recorrido\n[2] Por ID de imagen\n[3] Por ID de capa\n[4] Filtrar por usuario\nSelección: ")
            if so == "1": GenImg.x_rec_lim(ab_c, input("Método (preorden, inorden, postorden): "), int(input("Tope: ")))
            elif so == "2": GenImg.x_ls_im(ls_i, int(input("ID Imagen: ")))
            elif so == "3": GenImg.x_cp(ab_c, int(input("ID Capa: ")))
            elif so == "4": GenImg.x_usr(ab_u, ls_i, input("Usuario: "), int(input("ID Imagen: ")))
            
        elif op == "3":
            so = input("\n[1] Nuevo Usuario\n[2] Actualizar Usuario\n[3] Borrar Usuario\n[4] Asignar Imagen a Usuario\n[5] Quitar Imagen a Usuario\nSelección: ")
            if so == "1": GtCRUD.add_u(ab_u, input("Nombre de usuario: "))
            elif so == "2": GtCRUD.mod_u(ab_u, input("Usuario actual: "), input("Usuario nuevo: "))
            elif so == "3": GtCRUD.del_u(ab_u, input("Usuario a borrar: "))
            elif so == "4": GtCRUD.add_i(ls_i, ab_u, ab_c, input("Usuario: "), int(input("ID Imagen: ")), [int(x.strip()) for x in input("Capas CSV (ej. 1,2): ").split(',')])
            elif so == "5": GtCRUD.del_i(ls_i, ab_u, input("Usuario: "), int(input("ID Imagen: ")))
            
        elif op == "4":
            so = input("\n[1] Listado de imágenes\n[2] Jerarquía de capas\n[3] Estructura de capa (Matriz)\n[4] Vínculo imagen-jerarquía\n[5] Jerarquía de usuarios\nSelección: ")
            if so == "1": RepGvz.v_ls_i(ls_i)
            elif so == "2": RepGvz.v_ab_c(ab_c)
            elif so == "3": RepGvz.v_cp(ab_c, int(input("ID Capa: ")))
            elif so == "4": RepGvz.v_im_ab(ab_c, ls_i, int(input("ID Imagen: ")))
            elif so == "5": RepGvz.v_ab_u(ab_u)
            
        elif op == "5": break

if __name__ == "__main__":
    cnl_prnl()