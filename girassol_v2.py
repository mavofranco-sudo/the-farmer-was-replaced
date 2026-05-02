import campo
import megafazenda

_tem_crescendo = [False]
_petalas_lista = [[]]

# fatias fixas para colheita paralela (resetadas antes de cada colheita)
_f0  = [[]]
_f1  = [[]]
_f2  = [[]]
_f3  = [[]]
_f4  = [[]]
_f5  = [[]]
_f6  = [[]]
_f7  = [[]]
_f8  = [[]]
_f9  = [[]]
_f10 = [[]]
_f11 = [[]]
_f12 = [[]]
_f13 = [[]]
_f14 = [[]]
_f15 = [[]]
_f16 = [[]]
_f17 = [[]]
_f18 = [[]]
_f19 = [[]]
_f20 = [[]]
_f21 = [[]]
_f22 = [[]]
_f23 = [[]]
_f24 = [[]]
_f25 = [[]]
_f26 = [[]]
_f27 = [[]]
_f28 = [[]]
_f29 = [[]]
_f30 = [[]]
_f31 = [[]]

def _planta_celula():
	tipo = get_entity_type()
	if tipo == None:
		if num_items(Items.Carrot) > 0:
			campo.till_ate_soil()
			plant(Entities.Sunflower)
			campo._agua()
		return
	if tipo != Entities.Sunflower:
		if can_harvest():
			harvest()
		if num_items(Items.Carrot) > 0:
			campo.till_ate_soil()
			plant(Entities.Sunflower)
			campo._agua()
		return
	campo._agua()

def _verifica_crescimento():
	tipo = get_entity_type()
	if tipo == Entities.Sunflower:
		if not can_harvest():
			campo._agua()
			_tem_crescendo[0] = True

def _campo_pronto():
	_tem_crescendo[0] = False
	megafazenda.paraleliza_blocos(_verifica_crescimento)
	return not _tem_crescendo[0]

def _coleta_petalas():
	tipo = get_entity_type()
	if tipo == Entities.Sunflower:
		if can_harvest():
			p = measure()
			if p == None:
				p = 0
			x = get_pos_x()
			y = get_pos_y()
			_petalas_lista[0].append([p, x, y])

def _ordena_decrescente(lista):
	i = 1
	while i < len(lista):
		chave = lista[i]
		j = i - 1
		while j >= 0 and lista[j][0] < chave[0]:
			lista[j + 1] = lista[j]
			j -= 1
		lista[j + 1] = chave
		i += 1

def _colhe_lista(lst):
	for item in lst:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _c0():  _colhe_lista(_f0[0])
def _c1():  _colhe_lista(_f1[0])
def _c2():  _colhe_lista(_f2[0])
def _c3():  _colhe_lista(_f3[0])
def _c4():  _colhe_lista(_f4[0])
def _c5():  _colhe_lista(_f5[0])
def _c6():  _colhe_lista(_f6[0])
def _c7():  _colhe_lista(_f7[0])
def _c8():  _colhe_lista(_f8[0])
def _c9():  _colhe_lista(_f9[0])
def _c10(): _colhe_lista(_f10[0])
def _c11(): _colhe_lista(_f11[0])
def _c12(): _colhe_lista(_f12[0])
def _c13(): _colhe_lista(_f13[0])
def _c14(): _colhe_lista(_f14[0])
def _c15(): _colhe_lista(_f15[0])
def _c16(): _colhe_lista(_f16[0])
def _c17(): _colhe_lista(_f17[0])
def _c18(): _colhe_lista(_f18[0])
def _c19(): _colhe_lista(_f19[0])
def _c20(): _colhe_lista(_f20[0])
def _c21(): _colhe_lista(_f21[0])
def _c22(): _colhe_lista(_f22[0])
def _c23(): _colhe_lista(_f23[0])
def _c24(): _colhe_lista(_f24[0])
def _c25(): _colhe_lista(_f25[0])
def _c26(): _colhe_lista(_f26[0])
def _c27(): _colhe_lista(_f27[0])
def _c28(): _colhe_lista(_f28[0])
def _c29(): _colhe_lista(_f29[0])
def _c30(): _colhe_lista(_f30[0])
def _c31(): _colhe_lista(_f31[0])

_refs_f = [_f0,_f1,_f2,_f3,_f4,_f5,_f6,_f7,_f8,_f9,_f10,_f11,_f12,_f13,_f14,_f15,
           _f16,_f17,_f18,_f19,_f20,_f21,_f22,_f23,_f24,_f25,_f26,_f27,_f28,_f29,_f30,_f31]
_funcs_c = [_c0,_c1,_c2,_c3,_c4,_c5,_c6,_c7,_c8,_c9,_c10,_c11,_c12,_c13,_c14,_c15,
            _c16,_c17,_c18,_c19,_c20,_c21,_c22,_c23,_c24,_c25,_c26,_c27,_c28,_c29,_c30,_c31]

def _colhe_por_petalas():
	# 1) coleta medicoes em paralelo
	_petalas_lista[0] = []
	megafazenda.paraleliza_blocos(_coleta_petalas)

	lista = _petalas_lista[0]
	total = len(lista)
	if total == 0:
		print("    [girassol] nenhum girassol para colher")
		return 0

	# 2) ordena decrescente por petalas
	_ordena_decrescente(lista)

	# 3) distribui em fatias por referencia direta
	nd = max_drones()
	if nd < 1:
		nd = 1
	if nd > 32:
		nd = 32

	tam_fatia = total // nd
	if tam_fatia < 1:
		tam_fatia = 1

	i = 0
	while i < nd:
		inicio = i * tam_fatia
		fim = inicio + tam_fatia
		if i == nd - 1:
			fim = total
		if inicio < total:
			_refs_f[i][0] = lista[inicio:fim]
		else:
			_refs_f[i][0] = []
		i += 1

	# 4) spawna drones para colher em paralelo
	drones = []
	i = 0
	while i < nd:
		if len(_refs_f[i][0]) > 0:
			primeiro = _refs_f[i][0][0]
			campo.vai_para(primeiro[1], primeiro[2])
			drone = spawn_drone(_funcs_c[i])
			if drone:
				drones.append(drone)
			else:
				_funcs_c[i]()
		i += 1

	for d in drones:
		wait_for(d)

	return total

def tem_cenouras_suficientes():
	tam = get_world_size()
	return num_items(Items.Carrot) >= tam * tam

def um_ciclo_girassol():
	if not tem_cenouras_suficientes():
		return False

	t_inicio = time()

	megafazenda.paraleliza_blocos(_planta_celula)

	t_plantio = time()

	while not _campo_pronto():
		pass

	t_crescido = time()

	colhidos = _colhe_por_petalas()

	t_fim = time()

	duracao = t_fim - t_inicio
	if duracao < 0.001:
		duracao = 0.001
	por_min = int(colhidos * 60 / duracao)

	print("    [girassol] colhidos=" + str(colhidos) +
		" tempo=" + str(int(duracao * 1000)) + "ms" +
		" plantio=" + str(int((t_plantio - t_inicio) * 1000)) + "ms" +
		" crescimento=" + str(int((t_crescido - t_plantio) * 1000)) + "ms" +
		" colheita=" + str(int((t_fim - t_crescido) * 1000)) + "ms" +
		" ritmo=" + str(por_min) + "/min")

	return True

def modo_girassol(objetivo):
	while num_items(Items.Power) < objetivo:
		if not tem_cenouras_suficientes():
			print("    [girassol] sem cenouras (power=" +
				str(num_items(Items.Power)) + " obj=" + str(objetivo) + ")")
			return
		ok = um_ciclo_girassol()
		if not ok:
			print("    [girassol] ciclo falhou, abortando")
			return
