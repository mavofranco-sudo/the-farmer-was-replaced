import megafazenda

n = 0
metade_n = 0

direcoes = [North, South, East, West]
opostos = {
	North: South,
	South: North,
	East: West,
	West: East
}
deltas = {
	North: [0, 1],
	South: [0, -1],
	East: [1, 0],
	West: [-1, 0]
}

def inicializa():
	global n
	global metade_n
	n = get_world_size()
	metade_n = n // 2

def movimento(acao):
	for _ in range(n):
		for _ in range(n - 1):
			acao()
			move(North)
		acao()
		move(East)

def movimento_linha(acao):
	for _ in range(n - 1):
		acao()
		move(East)
	acao()

def _vai_para_abs(x_destino, y_destino, tam):
	metade = tam // 2
	x = get_pos_x()
	y = get_pos_y()

	dx = x_destino - x
	if dx > metade:
		dx = dx - tam
	elif dx < -metade:
		dx = dx + tam

	dy = y_destino - y
	if dy > metade:
		dy = dy - tam
	elif dy < -metade:
		dy = dy + tam

	if dx > 0:
		for _ in range(dx):
			move(East)
	elif dx < 0:
		for _ in range(-dx):
			move(West)

	if dy > 0:
		for _ in range(dy):
			move(North)
	elif dy < 0:
		for _ in range(-dy):
			move(South)

# acoes diretas para paraleliza_blocos (sem aninhamento)
def _faz_till():
	till()

def _faz_colhe():
	colhe()

def ara():
	megafazenda.paraleliza_blocos(_faz_till)

def limpa():
	megafazenda.paraleliza_blocos(_faz_colhe)

def colhe():
	while get_entity_type() and not can_harvest():
		_agua()
	if get_entity_type():
		harvest()

def proximo(x, y, direcao, passos=1):
	delta = deltas[direcao]
	x_delta = delta[0]
	y_delta = delta[1]
	return [x + passos * x_delta, y + passos * y_delta]

def distancia(x1, y1, x2, y2):
	return abs(x2 - x1) + abs(y2 - y1)

def define_dimensoes(p, p_destino, direcao):
	if p_destino < p:
		direcao = opostos[direcao]
	dist = abs(p_destino - p)
	if dist > metade_n:
		dist = n - dist
		direcao = opostos[direcao]
	return [dist, direcao]

def vai_para(x_destino, y_destino):
	tam = get_world_size()
	_vai_para_abs(x_destino, y_destino, tam)

def _agua():
	if num_items(Items.Water) > 0 and get_water() <= 0.75:
		use_item(Items.Water)

def _fertiliza():
	if num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)

def cultiva(planta, fertilizante=False):
	if num_unlocked(Unlocks.Plant):
		plant(planta)
	_agua()
	if fertilizante:
		_fertiliza()

def till_ate_soil():
	while get_ground_type() != Grounds.Soil:
		till()

def cultiva_arado(planta, fertilizante=False):
	till_ate_soil()
	if num_unlocked(Unlocks.Plant):
		plant(planta)
	_agua()
	if fertilizante:
		_fertiliza()

def colhe_e_cultiva(planta, fertilizante=False):
	colhe()
	cultiva(planta, fertilizante)

def colhe_e_cultiva_arado(planta, fertilizante=False):
	colhe()
	till_ate_soil()
	if num_unlocked(Unlocks.Plant):
		plant(planta)
	_agua()
	if fertilizante:
		_fertiliza()
