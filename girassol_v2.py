import campo
import megafazenda

_girassois = {}

def _inicializa_celula():
	tipo = get_entity_type()
	if tipo == Entities.Sunflower:
		if can_harvest():
			p = measure()
			if p == None:
				p = 7
			_girassois[p].add((get_pos_x(), get_pos_y()))
		else:
			campo._agua()
		return
	if tipo != None:
		if can_harvest():
			harvest()
	if get_ground_type() != Grounds.Soil:
		till()
	if get_ground_type() == Grounds.Soil:
		if num_items(Items.Carrot) > 0:
			plant(Entities.Sunflower)
			campo._agua()

def _tarefa_plantio():
	campo.movimento_linha(_inicializa_celula)
	return _girassois

def _constroi_resultados(resultados):
	for resultado in resultados:
		if resultado == None:
			continue
		i = 7
		while i <= 15:
			for par in resultado[i]:
				_girassois[i].add(par)
			i += 1

def _colhe_uma_passagem():
	# monta lista ordenada 15->7 e percorre 1 unica vez
	ordenadas = []
	p = 15
	while p >= 7:
		for par in _girassois[p]:
			ordenadas.append((par[0], par[1]))
		p -= 1

	total = 0
	for par in ordenadas:
		campo.vai_para(par[0], par[1])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()
				total += 1
	return total

def tem_cenouras_suficientes():
	tam = get_world_size()
	return num_items(Items.Carrot) >= tam * tam

def modo_girassol(objetivo):
	i = 7
	while i <= 15:
		_girassois[i] = set()
		i += 1

	ciclos = 0

	while num_items(Items.Power) < objetivo:
		if not tem_cenouras_suficientes():
			print("    [girassol] sem cenouras (power=" + str(num_items(Items.Power) // 1) + " obj=" + str(objetivo // 1) + ")")
			return

		t0 = get_time()
		resultados = megafazenda.paraleliza_linha(_tarefa_plantio)
		_constroi_resultados(resultados)
		t_plantio = get_time()

		total = _colhe_uma_passagem()

		p = 15
		while p >= 7:
			_girassois[p] = set()
			p -= 1

		t_fim = get_time()
		ciclos += 1
		dur = t_fim - t0
		dur_plantio = t_plantio - t0
		dur_colh = t_fim - t_plantio
		por_min = 0
		if dur > 0:
			por_min = (total * 60) // dur
		print("    [girassol] ciclo=" + str(ciclos) +
			" colhidos=" + str(total) +
			" power=" + str(num_items(Items.Power) // 1) + "/" + str(objetivo // 1) +
			" plantio=" + str(dur_plantio * 1000 // 1) + "ms" +
			" colh=" + str(dur_colh * 1000 // 1) + "ms" +
			" ritmo=" + str(por_min) + "/min")
