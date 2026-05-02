# ordem_errada.py
# Conquista: "Ordem errada"
# Organiza o campo cheio de cactos na ordem ERRADA:
# maior no SW, menor no NE (inverso da ordem correta)

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

# === PLANTAR E ESPERAR MADUROS ===
def _cria_faixa(x_ini, x_fim):
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
				if get_entity_type() != Entities.Cactus:
					plant(Entities.Cactus)
				y += 1
			x += 1
		# espera maduros na faixa
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

def _planta_e_espera():
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
		drones.append(_spawn(_cria_faixa(x_ini, x_fim)))
		i += 1
	_wait(drones)

# === SHEARSORT INVERTIDO ===
# ordem errada: maior no SW, menor no NE
# troca se vizinho ao Norte for MENOR que atual (queremos Norte <= atual)
# troca se vizinho ao Leste for MENOR que atual (queremos Leste <= atual)

def _cria_ord_linha_inv(y, tam):
	def fn():
		trocou = True
		while trocou:
			trocou = False
			x = 0
			while x < tam - 1:
				_vai(x, y)
				ve = measure(East)
				vm = measure()
				# ordem errada: queremos vm <= ve, ou seja East menor => troca se vm < ve
				if ve != None and vm != None and vm < ve:
					swap(East)
					trocou = True
				x += 1
	return fn

def _cria_ord_coluna_inv(x, tam):
	def fn():
		trocou = True
		while trocou:
			trocou = False
			y = 0
			while y < tam - 1:
				_vai(x, y)
				vn = measure(North)
				vm = measure()
				# ordem errada: queremos vm >= vn, ou seja Norte menor => troca se vm < vn
				if vn != None and vm != None and vm < vn:
					swap(North)
					trocou = True
				y += 1
	return fn

def _shearsort_invertido():
	tam = get_world_size()
	passes = tam // 2 + 1
	p = 0
	while p < passes:
		drones = []
		y = 0
		while y < tam:
			drones.append(_spawn(_cria_ord_linha_inv(y, tam)))
			y += 1
		_wait(drones)
		drones = []
		x = 0
		while x < tam:
			drones.append(_spawn(_cria_ord_coluna_inv(x, tam)))
			x += 1
		_wait(drones)
		p += 1

# === MAIN ===
print("[ordem_errada] plantando cactos...")
_planta_e_espera()
print("[ordem_errada] ordenando ao contrario...")
_shearsort_invertido()
print("[ordem_errada] campo organizado na ordem errada!")
