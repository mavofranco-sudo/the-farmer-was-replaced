# cacto.py

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

# === FASE 1+2: PLANTAR E ESPERAR EM PARALELO POR FAIXA ===
# cada drone planta sua faixa e fica num loop colhendo+replantando
# ate que toda sua faixa esteja madura, ai para
def _cria_faixa_planta_espera(x_ini, x_fim):
	def fn():
		tam = get_world_size()
		# primeiro: prepara e planta toda a faixa
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
		# segundo: fica varrendo a faixa ate todos maduros
		prontos = False
		while not prontos:
			prontos = True
			x = x_ini
			while x < x_fim:
				y = 0
				while y < tam:
					_vai(x, y)
					if not can_harvest():
						prontos = False
					y += 1
				x += 1
	return fn

def _planta_e_espera_paralelo():
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
		drones.append(_spawn(_cria_faixa_planta_espera(x_ini, x_fim)))
		i += 1
	_wait(drones)

# === FASE 3: SHEARSORT 2D PARALELO ===
def _cria_ord_linha(y, tam):
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
		drones = []
		y = 0
		while y < tam:
			drones.append(_spawn(_cria_ord_linha(y, tam)))
			y += 1
		_wait(drones)
		drones = []
		x = 0
		while x < tam:
			drones.append(_spawn(_cria_ord_coluna(x, tam)))
			x += 1
		_wait(drones)
		p += 1

# === FASE 4: COLHER ===
def _colhe():
	_vai(0, 0)
	harvest()

# === MODO CACTO ===
def modo_cacto(objetivo):
	while num_items(Items.Cactus) < objetivo:
		antes = num_items(Items.Cactus)
		tam = get_world_size()
		print("  [cacto] plantando e esperando maduros...")
		_planta_e_espera_paralelo()
		print("  [cacto] ordenando (shearsort)...")
		_shearsort()
		print("  [cacto] colhendo...")
		_colhe()
		depois = num_items(Items.Cactus)
		print("  [cacto] +cactos=" + str(depois - antes) + " total=" + str(depois) + "/" + str(objetivo))
