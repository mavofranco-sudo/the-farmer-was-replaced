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

# colhe uma lista de (x,y) passada via closure
def _cria_colheita_lista(celulas):
	def funcao():
		for par in celulas:
			campo.vai_para(par[0], par[1])
			if get_entity_type() == Entities.Sunflower:
				if can_harvest():
					harvest()
	return funcao

def _colhe_wave_paralelo(celulas):
	# divide as celulas entre nd drones e espera todos terminarem
	if len(celulas) == 0:
		return
	nd = max_drones()
	if nd < 1:
		nd = 1
	tam = len(celulas) // nd
	if tam < 1:
		tam = 1
	drones = []
	i = 0
	while i < nd:
		inicio = i * tam
		if i == nd - 1:
			fim = len(celulas)
		else:
			fim = inicio + tam
		if inicio >= len(celulas):
			i += 1
			continue
		fatia = celulas[inicio:fim]
		tarefa = _cria_colheita_lista(fatia)
		drone = spawn_drone(tarefa)
		if drone:
			drones.append(drone)
		else:
			tarefa()
		i += 1
	for d in drones:
		wait_for(d)

def _colhe_por_waves():
	# colhe nivel por nivel (15->7), esperando todos os drones de cada nivel
	# isso garante o bonus 8x: nenhum p=14 e colhido antes de todos p=15
	total = 0
	p = 15
	while p >= 7:
		celulas = list(_girassois[p])
		if len(celulas) > 0:
			_colhe_wave_paralelo(celulas)
			total += len(celulas)
		p -= 1
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

		total = _colhe_por_waves()

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
