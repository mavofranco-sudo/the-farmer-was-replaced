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

# modo continuo: cada drone faz sua faixa em loop: colhe se maduro, replanta, agua
# sem ordenacao global, sem waves, sem bonus 8x
def _cria_loop_faixa(x_ini, x_fim, y_ini, y_fim, ciclos):
	def funcao():
		c = 0
		while c < ciclos:
			y = y_ini
			while y < y_fim:
				x = x_ini
				while x < x_fim:
					campo.vai_para(x, y)
					tipo = get_entity_type()
					if tipo == Entities.Sunflower:
						if can_harvest():
							harvest()
							if get_ground_type() != Grounds.Soil:
								till()
							if num_items(Items.Carrot) > 0:
								plant(Entities.Sunflower)
								campo._agua()
						else:
							campo._agua()
					elif tipo == None:
						if get_ground_type() != Grounds.Soil:
							till()
						if num_items(Items.Carrot) > 0:
							plant(Entities.Sunflower)
							campo._agua()
					x += 1
				y += 1
			c += 1
	return funcao

def _colhe_por_waves():
	total = 0
	p = 15
	while p >= 7:
		for par in _girassois[p]:
			campo.vai_para(par[0], par[1])
			if get_entity_type() == Entities.Sunflower:
				if can_harvest():
					harvest()
					total += 1
		p -= 1
	return total

def tem_cenouras_suficientes():
	tam = get_world_size()
	return num_items(Items.Carrot) >= tam * tam

def modo_continuo(objetivo, ciclos_por_drone):
	# cada drone faz sua faixa por ciclos_por_drone voltas sem parar
	tam = get_world_size()
	nd = max_drones()
	if nd < 1:
		nd = 1
	faixa = tam // nd
	if faixa < 1:
		faixa = 1

	t0 = get_time()
	drones = []
	i = 0
	while i < nd:
		x_ini = i * faixa
		x_fim = x_ini + faixa
		if i == nd - 1:
			x_fim = tam
		tarefa = _cria_loop_faixa(x_ini, x_fim, 0, tam, ciclos_por_drone)
		drone = spawn_drone(tarefa)
		if drone:
			drones.append(drone)
		else:
			tarefa()
		i += 1

	for d in drones:
		wait_for(d)

	t_fim = get_time()
	dur = t_fim - t0
	power_atual = num_items(Items.Power) // 1
	por_min = 0
	if dur > 0:
		por_min = (power_atual * 60) // dur
	print("    [girassol-continuo] power=" + str(power_atual) +
		" dur=" + str(dur * 1000 // 1) + "ms" +
		" ritmo~=" + str(por_min) + "/min")

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

		# usa modo continuo: 32 drones, 3 ciclos cada
		modo_continuo(objetivo, 3)

		t_fim = get_time()
		ciclos += 1
		dur = t_fim - t0
		por_min = 0
		if dur > 0:
			por_min = (num_items(Items.Power) * 60) // dur
		print("    [girassol] ciclo=" + str(ciclos) +
			" power=" + str(num_items(Items.Power) // 1) + "/" + str(objetivo // 1) +
			" dur=" + str(dur * 1000 // 1) + "ms" +
			" ritmo~=" + str(por_min) + "/min")
