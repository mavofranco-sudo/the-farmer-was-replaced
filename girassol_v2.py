import campo
import megafazenda

def tem_cenouras_suficientes():
	tam = get_world_size()
	return num_items(Items.Carrot) >= tam * tam

def _faz_celula_girassol():
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
	else:
		if tipo != None:
			if can_harvest():
				harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) > 0:
			plant(Entities.Sunflower)
			campo._agua()

# usa argumentos default para capturar valores no momento da criacao
def _cria_faixa(cols, tam, ciclos, _cols=None, _tam=None, _ciclos=None):
	if _cols == None:
		_cols = cols
	if _tam == None:
		_tam = tam
	if _ciclos == None:
		_ciclos = ciclos
	def funcao():
		c = 0
		while c < _ciclos:
			y = 0
			while y < _tam:
				for x in _cols:
					campo.vai_para(x, y)
					_faz_celula_girassol()
				y += 1
			c += 1
	return funcao

def modo_girassol(objetivo):
	ciclo = 0
	while num_items(Items.Power) < objetivo:
		if not tem_cenouras_suficientes():
			print("    [girassol] sem cenouras (power=" + str(num_items(Items.Power) // 1) + " obj=" + str(objetivo // 1) + ")")
			return

		tam = get_world_size()
		nd = max_drones()
		if nd < 1:
			nd = 1

		# divide colunas entre drones — lista de colunas por drone
		faixa = tam // nd
		if faixa < 1:
			faixa = 1

		t0 = get_time()
		drones = []
		i = 0
		while i < nd:
			x_ini = i * faixa
			if i == nd - 1:
				x_fim = tam
			else:
				x_fim = x_ini + faixa
			# monta lista de colunas desse drone
			cols = []
			x = x_ini
			while x < x_fim:
				cols.append(x)
				x += 1
			tarefa = _cria_faixa(cols, tam, 3)
			drone = spawn_drone(tarefa)
			if drone:
				drones.append(drone)
			else:
				tarefa()
			i += 1

		for d in drones:
			wait_for(d)

		t_fim = get_time()
		ciclo += 1
		dur = t_fim - t0
		por_min = 0
		if dur > 0:
			por_min = (num_items(Items.Power) * 60) // dur
		print("    [girassol] ciclo=" + str(ciclo) +
			" power=" + str(num_items(Items.Power) // 1) + "/" + str(objetivo // 1) +
			" dur=" + str(dur * 1000 // 1) + "ms")
