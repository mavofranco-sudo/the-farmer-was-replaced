# cacto.py
# Planta, ordena (shearsort 2D) e colhe com bonus n²

def _vai(x, y):
	cx = get_pos_x()
	cy = get_pos_y()
	while cx < x:
		move(East)
		cx += 1
	while cx > x:
		move(West)
		cx -= 1
	while cy < y:
		move(North)
		cy += 1
	while cy > y:
		move(South)
		cy -= 1

def _spawn(fn):
	d = spawn_drone(fn)
	if d:
		return d
	fn()
	return None

def _wait(drones):
	for d in drones:
		if d:
			wait_for(d)

# === FASE 1: PLANTAR EM PARALELO ===
def _cria_planta_faixa(x_ini, x_fim):
	def fn():
		tam = get_world_size()
		x = x_ini
		while x < x_fim:
			y = 0
			while y < tam:
				_vai(x, y)
				if get_ground_type() != Grounds.Soil:
					if can_harvest():
						harvest()
					till()
				else:
					if can_harvest():
						harvest()
				if num_items(Items.Water) > 0:
					use_item(Items.Water)
				if num_items(Items.Fertilizer) > 0:
					use_item(Items.Fertilizer)
				if get_entity_type() != Entities.Cactus:
					plant(Entities.Cactus)
				y += 1
			x += 1
	return fn

def _planta_paralelo():
	tam = get_world_size()
	nd = max_drones()
	if nd < 1:
		nd = 1
	faixa = tam // nd
	if faixa < 1:
		faixa = 1
	drones = []
	i = 0
	while i < nd:
		x_ini = i * faixa
		if i == nd - 1:
			x_fim = tam
		else:
			x_fim = x_ini + faixa
		drones.append(_spawn(_cria_planta_faixa(x_ini, x_fim)))
		i += 1
	_wait(drones)

# === FASE 2: ESPERA TODOS MADUROS ===
def _espera_maduros():
	tam = get_world_size()
	todos_prontos = False
	while not todos_prontos:
		todos_prontos = True
		x = 0
		while x < tam:
			y = 0
			while y < tam:
				_vai(x, y)
				if not can_harvest():
					todos_prontos = False
				y += 1
			x += 1

# === FASE 3: SHEARSORT 2D PARALELO ===
# Ordena: grid[y][x] <= grid[y+1][x] (Norte maior) e grid[y][x] <= grid[y][x+1] (Leste maior)
# i.e. menor no SW, maior no NE

def _cria_ord_linha(y, tam):
	# ordena linha y: x cresce para Leste (menor a Oeste, maior a Leste)
	def fn():
		trocou = True
		while trocou:
			trocou = False
			x = 0
			while x < tam - 1:
				_vai(x, y)
				ve = measure(East)
				vm = measure()
				if ve != None and vm != None and vm > ve:
					swap(East)
					trocou = True
				x += 1
	return fn

def _cria_ord_coluna(x, tam):
	# ordena coluna x: y cresce para Norte (menor ao Sul, maior ao Norte)
	def fn():
		trocou = True
		while trocou:
			trocou = False
			y = 0
			while y < tam - 1:
				_vai(x, y)
				vn = measure(North)
				vm = measure()
				if vn != None and vm != None and vm > vn:
					swap(North)
					trocou = True
				y += 1
	return fn

def _shearsort():
	tam = get_world_size()
	passes = tam // 2 + 1
	p = 0
	while p < passes:
		# linhas em paralelo
		drones = []
		y = 0
		while y < tam:
			drones.append(_spawn(_cria_ord_linha(y, tam)))
			y += 1
		_wait(drones)
		# colunas em paralelo
		drones = []
		x = 0
		while x < tam:
			drones.append(_spawn(_cria_ord_coluna(x, tam)))
			x += 1
		_wait(drones)
		p += 1

# === FASE 4: COLHER ===
def _colhe():
	# basta colher 1 cacto — se ordenado, colhe todos recursivamente
	_vai(0, 0)
	harvest()

# === MODO CACTO COMPLETO ===
def modo_cacto(objetivo):
	while num_items(Items.Cactus) < objetivo:
		antes = num_items(Items.Cactus)
		print("  [cacto] plantando...")
		_planta_paralelo()
		print("  [cacto] esperando maduros...")
		_espera_maduros()
		print("  [cacto] ordenando...")
		_shearsort()
		print("  [cacto] colhendo...")
		_colhe()
		depois = num_items(Items.Cactus)
		tam = get_world_size()
		esperado = tam * tam * tam * tam
		print("  [cacto] colhido=" + str(depois - antes) + " esperado=" + str(esperado) + " total=" + str(depois))

def cacto():
	modo_cacto(get_world_size() ** 4)
