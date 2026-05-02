import campo
import chapeus
import megafazenda

_girassois = {}

def _inicializa_celula():
	campo.cultiva(Entities.Sunflower)
	p = measure()
	if p == None:
		p = 7
	return [p, get_pos_x(), get_pos_y()]

def _tarefa_linha():
	tam = get_world_size()
	resultado = {}
	i = 7
	while i <= 15:
		resultado[i] = []
		i += 1
	x = 0
	while x < tam:
		campo.vai_para(x, get_pos_y())
		campo.cultiva(Entities.Sunflower)
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				p = measure()
				if p == None:
					p = 7
				if p < 7:
					p = 7
				if p > 15:
					p = 15
				resultado[p].append([get_pos_x(), get_pos_y()])
		x += 1
	return resultado

def _constroi_grupos(resultados, grupos):
	for resultado in resultados:
		if resultado == None:
			continue
		i = 7
		while i <= 15:
			for item in resultado[i]:
				grupos[i].append(item)
			i += 1

def _tarefa_colheita(x, y):
	def funcao():
		campo.vai_para(x, y)
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()
	return chapeus.usa_e_faz(funcao)

def tem_cenouras_suficientes():
	tam = get_world_size()
	return num_items(Items.Carrot) >= tam * tam

def um_ciclo_girassol():
	if not tem_cenouras_suficientes():
		return False

	t0 = get_time()

	# planta e coleta medicoes por linha em paralelo
	resultados = megafazenda.paraleliza_linha(_tarefa_linha)

	t_plantio = get_time()

	# consolida grupos por numero de petalas
	grupos = {}
	i = 7
	while i <= 15:
		grupos[i] = []
		i += 1
	_constroi_grupos(resultados, grupos)

	# verifica se tem girassois maduros
	total = 0
	i = 7
	while i <= 15:
		total += len(grupos[i])
		i += 1

	if total == 0:
		# nenhum maduro ainda - aguarda e tenta de novo sem replantio
		while not _todos_maduros():
			pass
		t_crescido = get_time()
		# recoleta apos crescer
		i = 7
		while i <= 15:
			grupos[i] = []
			i += 1
		_coleta_serie(grupos)
		total = 0
		i = 7
		while i <= 15:
			total += len(grupos[i])
			i += 1
	else:
		t_crescido = t_plantio

	# colhe do maior para o menor - preserva bonus 8x
	p = 15
	while p >= 7:
		if len(grupos[p]) > 0:
			drones = []
			for item in grupos[p]:
				x = item[0]
				y = item[1]
				drone = spawn_drone(_tarefa_colheita(x, y))
				if drone:
					drones.append(drone)
				else:
					campo.vai_para(x, y)
					if get_entity_type() == Entities.Sunflower:
						if can_harvest():
							harvest()
			for d in drones:
				wait_for(d)
		p -= 1

	t_fim = get_time()
	dur_total = t_fim - t0
	dur_plantio = t_plantio - t0
	dur_cresc = t_crescido - t_plantio
	dur_colh = t_fim - t_crescido
	por_min = 0
	if dur_total > 0:
		por_min = (total * 60) // dur_total
	print("    [girassol] colhidos=" + str(total) +
		" total=" + str(dur_total * 1000 // 1) + "ms" +
		" plantio=" + str(dur_plantio * 1000 // 1) + "ms" +
		" cresc=" + str(dur_cresc * 1000 // 1) + "ms" +
		" colh=" + str(dur_colh * 1000 // 1) + "ms" +
		" ritmo=" + str(por_min) + "/min")
	return True

def _todos_maduros():
	tam = get_world_size()
	x = 0
	while x < tam:
		y = 0
		while y < tam:
			campo.vai_para(x, y)
			tipo = get_entity_type()
			if tipo == None:
				campo.till_ate_soil()
				if num_items(Items.Carrot) > 0:
					plant(Entities.Sunflower)
				return False
			if tipo == Entities.Sunflower:
				if not can_harvest():
					campo._agua()
					return False
			y += 1
		x += 1
	return True

def _coleta_serie(grupos):
	tam = get_world_size()
	x = 0
	while x < tam:
		y = 0
		while y < tam:
			campo.vai_para(x, y)
			if get_entity_type() == Entities.Sunflower:
				if can_harvest():
					p = measure()
					if p == None:
						p = 7
					if p < 7:
						p = 7
					if p > 15:
						p = 15
					grupos[p].append([x, y])
			y += 1
		x += 1

def modo_girassol(objetivo):
	while num_items(Items.Power) < objetivo:
		if not tem_cenouras_suficientes():
			print("    [girassol] sem cenouras (power=" + str(num_items(Items.Power)) + " obj=" + str(objetivo) + ")")
			return
		ok = um_ciclo_girassol()
		if not ok:
			print("    [girassol] ciclo falhou, abortando")
			return
