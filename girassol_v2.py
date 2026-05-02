import campo
import megafazenda

_tem_crescendo = [False]
_petalas_lista = [[]]

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

# colheita por fatias: cada funcao colhe uma fatia da lista ordenada
# usando indices fixos para evitar closure em loop
_fatias = [[]]

def _colhe_fatia_0():
	for item in _fatias[0]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_1():
	for item in _fatias[1]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_2():
	for item in _fatias[2]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_3():
	for item in _fatias[3]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_4():
	for item in _fatias[4]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_5():
	for item in _fatias[5]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_6():
	for item in _fatias[6]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_7():
	for item in _fatias[7]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_8():
	for item in _fatias[8]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_9():
	for item in _fatias[9]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_10():
	for item in _fatias[10]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_11():
	for item in _fatias[11]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_12():
	for item in _fatias[12]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_13():
	for item in _fatias[13]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_14():
	for item in _fatias[14]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_15():
	for item in _fatias[15]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_16():
	for item in _fatias[16]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_17():
	for item in _fatias[17]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_18():
	for item in _fatias[18]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_19():
	for item in _fatias[19]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_20():
	for item in _fatias[20]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_21():
	for item in _fatias[21]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_22():
	for item in _fatias[22]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_23():
	for item in _fatias[23]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_24():
	for item in _fatias[24]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_25():
	for item in _fatias[25]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_26():
	for item in _fatias[26]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_27():
	for item in _fatias[27]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_28():
	for item in _fatias[28]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_29():
	for item in _fatias[29]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_30():
	for item in _fatias[30]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

def _colhe_fatia_31():
	for item in _fatias[31]:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()

_funcs_fatia = [
	_colhe_fatia_0,  _colhe_fatia_1,  _colhe_fatia_2,  _colhe_fatia_3,
	_colhe_fatia_4,  _colhe_fatia_5,  _colhe_fatia_6,  _colhe_fatia_7,
	_colhe_fatia_8,  _colhe_fatia_9,  _colhe_fatia_10, _colhe_fatia_11,
	_colhe_fatia_12, _colhe_fatia_13, _colhe_fatia_14, _colhe_fatia_15,
	_colhe_fatia_16, _colhe_fatia_17, _colhe_fatia_18, _colhe_fatia_19,
	_colhe_fatia_20, _colhe_fatia_21, _colhe_fatia_22, _colhe_fatia_23,
	_colhe_fatia_24, _colhe_fatia_25, _colhe_fatia_26, _colhe_fatia_27,
	_colhe_fatia_28, _colhe_fatia_29, _colhe_fatia_30, _colhe_fatia_31,
]

def _colhe_por_petalas():
	# 1) coleta todas as medicoes em paralelo com todos os drones
	_petalas_lista[0] = []
	megafazenda.paraleliza_blocos(_coleta_petalas)

	lista = _petalas_lista[0]
	if len(lista) == 0:
		return

	# 2) ordena decrescente por petalas (maior bonus primeiro)
	_ordena_decrescente(lista)

	# 3) divide lista ordenada em fatias para cada drone
	nd = max_drones()
	if nd < 1:
		nd = 1
	tam_lista = len(lista)
	tam_fatia = tam_lista // nd
	if tam_fatia < 1:
		tam_fatia = 1

	# inicializa fatias vazias
	i = 0
	while i < 32:
		_fatias.append([])
		i += 1
	while len(_fatias) < 32:
		_fatias.append([])

	# distribui itens nas fatias
	i = 0
	while i < nd and i < 32:
		inicio = i * tam_fatia
		fim = inicio + tam_fatia
		if i == nd - 1:
			fim = tam_lista
		if inicio < tam_lista:
			_fatias[i] = lista[inicio:fim]
		else:
			_fatias[i] = []
		i += 1

	# 4) spawna um drone por fatia para colher em paralelo
	drones = []
	i = 0
	while i < nd and i < len(_funcs_fatia):
		if len(_fatias[i]) > 0:
			primeiro = _fatias[i][0]
			campo.vai_para(primeiro[1], primeiro[2])
			drone = spawn_drone(_funcs_fatia[i])
			if drone:
				drones.append(drone)
			else:
				_funcs_fatia[i]()
		i += 1

	for d in drones:
		wait_for(d)

def tem_cenouras_suficientes():
	tam = get_world_size()
	return num_items(Items.Carrot) >= tam * tam

def um_ciclo_girassol():
	if not tem_cenouras_suficientes():
		return False
	megafazenda.paraleliza_blocos(_planta_celula)
	while not _campo_pronto():
		pass
	_colhe_por_petalas()
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
