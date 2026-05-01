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

def movimento_bloco(num_linhas, num_colunas, acao):
	# percorre o bloco com dois for simples, sentido serpentina
	# garante que todas as celulas do bloco sejam visitadas
	x0 = get_pos_x()
	y0 = get_pos_y()
	for col in range(num_colunas):
		for lin in range(num_linhas):
			vai_para(x0 + col, y0 + lin)
			acao()

def _tarefa_ara():
	def funcao():
		def faz_till():
			till()
		movimento_bloco(megafazenda.linhas, megafazenda.colunas, faz_till)
	return funcao

def _tarefa_limpa():
	def funcao():
		def faz_colhe():
			colhe()
		movimento_bloco(megafazenda.linhas, megafazenda.colunas, faz_colhe)
	return funcao

def cria_movimento(acao):
	def funcao():
		movimento(acao)
	return funcao

def cria_movimento_linha(acao):
	def funcao():
		movimento_linha(acao)
	return funcao

def ara():
	megafazenda.paraleliza_blocos(_tarefa_ara())

def colhe():
	while get_entity_type() and not can_harvest():
		_agua()
	if get_entity_type():
		harvest()

def limpa():
	megafazenda.paraleliza_blocos(_tarefa_limpa())

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
	x = get_pos_x()
	y = get_pos_y()
	dims_h = define_dimensoes(x, x_destino, East)
	dims_v = define_dimensoes(y, y_destino, North)
	dist_horizontal = dims_h[0]
	dir_horizontal = dims_h[1]
	dist_vertical = dims_v[0]
	dir_vertical = dims_v[1]
	for _ in range(dist_horizontal):
		move(dir_horizontal)
	for _ in range(dist_vertical):
		move(dir_vertical)

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
