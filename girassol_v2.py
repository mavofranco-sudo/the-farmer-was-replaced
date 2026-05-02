import campo
import chapeus
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

# cada drone recebe sua faixa de celulas e colhe na ordem certa (15->7)
# a lista global _faixas_colheita[drone_idx] = lista ordenada de [p, x, y]
_faixas_colheita = {}

def _tarefa_colheita_faixa(idx):
	def funcao():
		faixa = _faixas_colheita[idx]
		# ordena por petalas decrescente dentro da faixa
		# insertion sort (sem sorted/lambda)
		i = 1
		while i < len(faixa):
			chave = faixa[i]
			j = i - 1
			while j >= 0 and faixa[j][0] < chave[0]:
				faixa[j + 1] = faixa[j]
				j -= 1
			faixa[j + 1] = chave
			i += 1
		for item in faixa:
			campo.vai_para(item[1], item[2])
			if get_entity_type() == Entities.Sunflower:
				if can_harvest():
					harvest()
	return chapeus.usa_e_faz(funcao)

def _colhe_paralelo():
	# monta lista global com todas as celulas maduras: [p, x, y]
	todas = []
	p = 15
	while p >= 7:
		for par in _girassois[p]:
			todas.append([p, par[0], par[1]])
		p -= 1

	total = len(todas)
	if total == 0:
		return 0

	nd = max_drones()
	if nd < 1:
		nd = 1

	# divide em nd faixas
	tam = total // nd
	if tam < 1:
		tam = 1

	i = 0
	while i < nd:
		inicio = i * tam
		fim = inicio + tam
		if i == nd - 1:
			fim = total
		if inicio < total:
			_faixas_colheita[i] = todas[inicio:fim]
		else:
			_faixas_colheita[i] = []
		i += 1

	drones = []
	i = 0
	while i < nd:
		if len(_faixas_colheita[i]) > 0:
			primeiro = _faixas_colheita[i][0]
			campo.vai_para(primeiro[1], primeiro[2])
			drone = spawn_drone(_tarefa_colheita_faixa(i))
			if drone:
				drones.append(drone)
			else:
				_tarefa_colheita_faixa(i)()
		i += 1

	for d in drones:
		wait_for(d)

	return total

def tem_cenouras_suficientes():
	tam = get_world_size()
	return num_items(Items.Carrot) >= tam * tam

def modo_girassol(objetivo):
	i = 7
	while i <= 15:
		_girassois[i] = set()
		i += 1

	t_total_inicio = get_time()
	ciclos = 0

	while num_items(Items.Power) < objetivo:
		if not tem_cenouras_suficientes():
			print("    [girassol] sem cenouras (power=" + str(num_items(Items.Power)) + " obj=" + str(objetivo) + ")")
			return

		t0 = get_time()
		resultados = megafazenda.paraleliza_linha(_tarefa_plantio)
		_constroi_resultados(resultados)
		t_plantio = get_time()

		total = _colhe_paralelo()

		# limpa para proximo ciclo
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
