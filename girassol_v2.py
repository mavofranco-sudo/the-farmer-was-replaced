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

# colhe todas as celulas maduras numa linha y, ordenando por petalas desc
def _cria_colheita_linha(y, celulas):
	# celulas = lista de [p, x] para essa linha
	def funcao():
		# ordena por petalas desc (insertion sort)
		i = 1
		while i < len(celulas):
			chave = celulas[i]
			j = i - 1
			while j >= 0 and celulas[j][0] < chave[0]:
				celulas[j + 1] = celulas[j]
				j -= 1
			celulas[j + 1] = chave
			i += 1
		for item in celulas:
			campo.vai_para(item[1], y)
			if get_entity_type() == Entities.Sunflower:
				if can_harvest():
					harvest()
	return chapeus.usa_e_faz(funcao)

def _colhe_paralelo():
	tam = get_world_size()

	# agrupa celulas maduras por linha y
	por_linha = {}
	p = 15
	while p >= 7:
		for par in _girassois[p]:
			x = par[0]
			y = par[1]
			if y not in por_linha:
				por_linha[y] = []
			por_linha[y].append([p, x])
		p -= 1

	total = 0
	for y in por_linha:
		total += len(por_linha[y])

	if total == 0:
		return 0

	nd = max_drones()
	if nd < 1:
		nd = 1

	# lista de linhas com celulas
	linhas = []
	for y in por_linha:
		linhas.append(y)

	# distribui linhas em nd grupos
	grupos = {}
	i = 0
	while i < nd:
		grupos[i] = []
		i += 1

	i = 0
	for y in linhas:
		grupos[i % nd].append(y)
		i += 1

	def _cria_colheita_grupo(grupo_linhas, dados_linhas):
		def funcao():
			for y in grupo_linhas:
				celulas = dados_linhas[y]
				# ordena por petalas desc
				i = 1
				while i < len(celulas):
					chave = celulas[i]
					j = i - 1
					while j >= 0 and celulas[j][0] < chave[0]:
						celulas[j + 1] = celulas[j]
						j -= 1
					celulas[j + 1] = chave
					i += 1
				for item in celulas:
					campo.vai_para(item[1], y)
					if get_entity_type() == Entities.Sunflower:
						if can_harvest():
							harvest()
		return chapeus.usa_e_faz(funcao)

	drones = []
	i = 0
	while i < nd:
		if len(grupos[i]) > 0:
			# posiciona drone no primeiro x,y do grupo para spawn eficiente
			primeira_linha = grupos[i][0]
			primeiro_x = por_linha[primeira_linha][0][1]
			campo.vai_para(primeiro_x, primeira_linha)
			tarefa = _cria_colheita_grupo(grupos[i], por_linha)
			drone = spawn_drone(tarefa)
			if drone:
				drones.append(drone)
			else:
				tarefa()
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
			print("    [girassol] sem cenouras (power=" + str(num_items(Items.Power) // 1) + " obj=" + str(objetivo // 1) + ")")
			return

		t0 = get_time()
		resultados = megafazenda.paraleliza_linha(_tarefa_plantio)
		_constroi_resultados(resultados)
		t_plantio = get_time()

		total = _colhe_paralelo()

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
