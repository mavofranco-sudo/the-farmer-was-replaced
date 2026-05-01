import campo
import megafazenda

def _planta_celula():
	tipo = get_entity_type()
	if tipo == None:
		if num_items(Items.Carrot) > 0:
			campo.till_ate_soil()
			plant(Entities.Sunflower)
	elif tipo != Entities.Sunflower:
		if can_harvest():
			harvest()
		if num_items(Items.Carrot) > 0:
			campo.till_ate_soil()
			plant(Entities.Sunflower)
	campo._agua()

def _rega_celula():
	if get_entity_type() == Entities.Sunflower:
		campo._agua()

def _campo_todo_crescido():
	tam = get_world_size()
	for x in range(tam):
		for y in range(tam):
			campo.vai_para(x, y)
			if get_entity_type() == Entities.Sunflower and not can_harvest():
				return False
	return True

def _colhe_por_ordem():
	tam = get_world_size()
	petalas = []
	for x in range(tam):
		for y in range(tam):
			campo.vai_para(x, y)
			if get_entity_type() == Entities.Sunflower and can_harvest():
				p = measure()
				if p == None:
					p = 7
				petalas.append([p, x, y])

	# ordena decrescente por petalas (maior primeiro = mais bonus)
	i = 1
	while i < len(petalas):
		chave = petalas[i]
		j = i - 1
		while j >= 0 and petalas[j][0] < chave[0]:
			petalas[j + 1] = petalas[j]
			j -= 1
		petalas[j + 1] = chave
		i += 1

	for item in petalas:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower and can_harvest():
			harvest()

def tem_cenouras_suficientes():
	tam = get_world_size()
	return num_items(Items.Carrot) >= tam * tam

def um_ciclo_girassol():
	megafazenda.paraleliza_blocos(_planta_celula)
	while not _campo_todo_crescido():
		megafazenda.paraleliza_blocos(_rega_celula)
	_colhe_por_ordem()

def modo_girassol(objetivo):
	while num_items(Items.Power) < objetivo:
		um_ciclo_girassol()
