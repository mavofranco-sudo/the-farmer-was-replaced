import campo
import megafazenda

_CUSTO_SEMENTE = 64

def _limpa_celula():
	if get_entity_type() != None and can_harvest():
		harvest()

def _planta_cacto():
	if num_items(Items.Pumpkin) < _CUSTO_SEMENTE:
		return
	tipo = get_entity_type()
	if tipo != None:
		if can_harvest():
			harvest()
		else:
			return
	campo.till_ate_soil()
	if num_unlocked(Unlocks.Plant):
		plant(Entities.Cactus)
	campo._agua()

def _rega_celula():
	campo._agua()

def _campo_todo_crescido():
	tem_algum = False
	tam = get_world_size()
	y = 0
	while y < tam:
		x = 0
		while x < tam:
			campo.vai_para(x, y)
			if get_entity_type() == Entities.Cactus:
				tem_algum = True
				if not can_harvest():
					return False
			x += 1
		y += 1
	return tem_algum

def _measure_safe(direcao=None):
	if direcao == None:
		val = measure()
	else:
		val = measure(direcao)
	if val == None:
		return 0
	return val

# ordena uma coluna inteira (bubble sort vertical)
def _cria_ordena_coluna(col, tam):
	def funcao():
		trocou = True
		while trocou:
			trocou = False
			j = 0
			while j < tam - 1:
				campo.vai_para(col, j)
				v_atual = _measure_safe()
				v_norte = measure(North)
				if v_norte != None and v_atual > v_norte:
					swap(North)
					trocou = True
				j += 1
	return funcao

# ordena uma linha inteira (bubble sort horizontal)
def _cria_ordena_linha(lin, tam):
	def funcao():
		trocou = True
		while trocou:
			trocou = False
			j = 0
			while j < tam - 1:
				campo.vai_para(j, lin)
				v_atual = _measure_safe()
				v_leste = measure(East)
				if v_leste != None and v_atual > v_leste:
					swap(East)
					trocou = True
				j += 1
	return funcao

def _ordena_campo_paralelo():
	tam = get_world_size()
	nd = max_drones()
	if nd < 1:
		nd = 1

	# fase 1: ordena todas as colunas em paralelo
	drones = []
	col = 0
	while col < tam:
		tarefa = _cria_ordena_coluna(col, tam)
		drone = spawn_drone(tarefa)
		if drone:
			drones.append(drone)
		else:
			tarefa()
		col += 1
	for d in drones:
		wait_for(d)

	# fase 2: ordena todas as linhas em paralelo
	drones = []
	lin = 0
	while lin < tam:
		tarefa = _cria_ordena_linha(lin, tam)
		drone = spawn_drone(tarefa)
		if drone:
			drones.append(drone)
		else:
			tarefa()
		lin += 1
	for d in drones:
		wait_for(d)

	# fase 3: reordena colunas (Shearsort: repete tam/2 vezes eh suficiente)
	passes = tam // 2
	if passes < 1:
		passes = 1
	p = 0
	while p < passes:
		drones = []
		col = 0
		while col < tam:
			tarefa = _cria_ordena_coluna(col, tam)
			drone = spawn_drone(tarefa)
			if drone:
				drones.append(drone)
			else:
				tarefa()
			col += 1
		for d in drones:
			wait_for(d)
		p += 1

def _aboboras_para_campo_cheio():
	tam = get_world_size()
	return tam * tam * _CUSTO_SEMENTE

def modo_cacto(objetivo):
	while num_items(Items.Cactus) < objetivo:
		aboboras_necessarias = _aboboras_para_campo_cheio()
		if num_items(Items.Pumpkin) < aboboras_necessarias:
			print("    [cacto] precisa de " + str(aboboras_necessarias) + " aboboras, tem " + str(num_items(Items.Pumpkin)))
			import abobora
			abobora.modo_abobora(aboboras_necessarias)

		t0 = get_time()
		megafazenda.paraleliza_blocos(_limpa_celula)
		megafazenda.paraleliza_blocos(_planta_cacto)
		t_plantio = get_time()

		while not _campo_todo_crescido():
			megafazenda.paraleliza_blocos(_rega_celula)
		t_crescido = get_time()

		_ordena_campo_paralelo()
		t_ordenado = get_time()

		campo.vai_para(0, 0)
		harvest()
		t_fim = get_time()

		print("    [cacto] plantio=" + str((t_plantio - t0) * 1000 // 1) + "ms" +
			" crescimento=" + str((t_crescido - t_plantio) * 1000 // 1) + "ms" +
			" ordenacao=" + str((t_ordenado - t_crescido) * 1000 // 1) + "ms" +
			" harvest=" + str((t_fim - t_ordenado) * 1000 // 1) + "ms" +
			" cactos=" + str(num_items(Items.Cactus)))
