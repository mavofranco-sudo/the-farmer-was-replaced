import campo
import chapeus
import megafazenda

_girassois = {}

def _inicializa_celula():
	tipo = get_entity_type()
	if tipo == Entities.Sunflower:
		# ja tem girassol - so mede e registra se maduro
		if can_harvest():
			p = measure()
			if p == None:
				p = 7
			_girassois[p].add((get_pos_x(), get_pos_y()))
		else:
			campo._agua()
		return
	# celula vazia ou outra planta - colhe se tiver, ara e planta
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

def _tarefa_colheita(x, y):
	def funcao():
		campo.vai_para(x, y)
		campo.colhe()
	return chapeus.usa_e_faz(funcao)

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

		total = 0
		p = 15
		while p >= 7:
			if len(_girassois[p]) > 0:
				drones = []
				for par in _girassois[p]:
					x = par[0]
					y = par[1]
					campo.vai_para(campo.metade_n, campo.metade_n)
					drone = None
					while not drone:
						drone = spawn_drone(_tarefa_colheita(x, y))
					drones.append(drone)
				for d in drones:
					wait_for(d)
				total += len(_girassois[p])
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
			" power=" + str(num_items(Items.Power)) + "/" + str(objetivo) +
			" total=" + str(dur * 1000 // 1) + "ms" +
			" plantio=" + str(dur_plantio * 1000 // 1) + "ms" +
			" colh=" + str(dur_colh * 1000 // 1) + "ms" +
			" ritmo=" + str(por_min) + "/min")
