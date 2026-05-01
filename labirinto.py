import campo
import megafazenda

# wall-following: gira à esquerda sempre que possível, senão vai reto, senão direita, senão volta
# sem loops no labirinto => wall-following garante achar o tesouro

# direcoes em ordem para rotacao: N, E, S, W (indices 0,1,2,3)
_dirs = [North, East, South, West]

def _vira_esquerda(idx):
	return (idx - 1) % 4

def _vira_direita(idx):
	return (idx + 1) % 4

def _vira_oposto(idx):
	return (idx + 2) % 4

def _navega_wall_follow(x_ini, y_ini):
	# wall-following: mantem a parede à esquerda
	# comeca olhando para North
	direcao_idx = 0

	passos = 0
	limite = get_world_size() * get_world_size() * 4

	while passos < limite:
		if get_entity_type() == Entities.Treasure:
			return True

		# tenta virar esquerda
		esq = _vira_esquerda(direcao_idx)
		if can_move(_dirs[esq]):
			direcao_idx = esq
			move(_dirs[direcao_idx])
			passos += 1
			continue

		# tenta ir reto
		if can_move(_dirs[direcao_idx]):
			move(_dirs[direcao_idx])
			passos += 1
			continue

		# tenta virar direita
		dir = _vira_direita(direcao_idx)
		if can_move(_dirs[dir]):
			direcao_idx = dir
			move(_dirs[direcao_idx])
			passos += 1
			continue

		# sem saida: vira oposto (voltou a um beco sem saida)
		direcao_idx = _vira_oposto(direcao_idx)
		move(_dirs[direcao_idx])
		passos += 1

	return False

def _custo_labirinto():
	# formula da documentacao: get_world_size() * 2^(num_unlocked(Mazes) - 1)
	tam = get_world_size()
	nivel = num_unlocked(Unlocks.Mazes)
	if nivel < 1:
		nivel = 1
	potencia = 1
	i = 0
	while i < nivel - 1:
		potencia = potencia * 2
		i += 1
	return tam * potencia

def _ciclo_drone(indice, nd, objetivo):
	custo = _custo_labirinto()
	tam = get_world_size()

	# calcula centro da regiao 2D deste drone
	cols, rows = _divisao_2d(tam, nd)
	w = (tam + cols - 1) // cols
	h = (tam + rows - 1) // rows
	col_grade = indice // rows
	row_grade = indice % rows
	x0 = col_grade * w
	y0 = row_grade * h
	x1 = x0 + w
	if x1 > tam:
		x1 = tam
	y1 = y0 + h
	if y1 > tam:
		y1 = tam
	cx = (x0 + x1) // 2
	cy = (y0 + y1) // 2

	# vai para o centro da regiao
	campo.vai_para(cx, cy)

	# garante WS suficiente para este drone
	if num_items(Items.Weird_Substance) < custo:
		return

	# planta Bush e cria labirinto
	if get_entity_type() != None:
		if can_harvest():
			harvest()

	plant(Entities.Bush)
	use_item(Items.Weird_Substance, custo)

	# navega ate o tesouro com wall-following
	x = get_pos_x()
	y = get_pos_y()
	achou = _navega_wall_follow(x, y)

	# colhe o tesouro (ou limpa se nao achou)
	if get_entity_type() != None and can_harvest():
		harvest()
	elif get_entity_type() != None:
		harvest()

	print("    [lab] drone=" + str(indice) + " gold=" + str(num_items(Items.Gold)) + " achou=" + str(achou))

def _divisao_2d(n, nd):
	melhor_c = nd
	melhor_r = 1
	c = 1
	while c <= nd:
		if nd % c == 0:
			r = nd // c
			d_atual = c - r
			if d_atual < 0:
				d_atual = -d_atual
			d_melhor = melhor_c - melhor_r
			if d_melhor < 0:
				d_melhor = -d_melhor
			if d_atual < d_melhor:
				melhor_c = c
				melhor_r = r
		c += 1
	return melhor_c, melhor_r

# 32 fabricas para paraleliza_blocos
def _fab_0(obj, nd):
	def t():
		_ciclo_drone(0, nd, obj)
	return t

def _fab_1(obj, nd):
	def t():
		_ciclo_drone(1, nd, obj)
	return t

def _fab_2(obj, nd):
	def t():
		_ciclo_drone(2, nd, obj)
	return t

def _fab_3(obj, nd):
	def t():
		_ciclo_drone(3, nd, obj)
	return t

def _fab_4(obj, nd):
	def t():
		_ciclo_drone(4, nd, obj)
	return t

def _fab_5(obj, nd):
	def t():
		_ciclo_drone(5, nd, obj)
	return t

def _fab_6(obj, nd):
	def t():
		_ciclo_drone(6, nd, obj)
	return t

def _fab_7(obj, nd):
	def t():
		_ciclo_drone(7, nd, obj)
	return t

def _fab_8(obj, nd):
	def t():
		_ciclo_drone(8, nd, obj)
	return t

def _fab_9(obj, nd):
	def t():
		_ciclo_drone(9, nd, obj)
	return t

def _fab_10(obj, nd):
	def t():
		_ciclo_drone(10, nd, obj)
	return t

def _fab_11(obj, nd):
	def t():
		_ciclo_drone(11, nd, obj)
	return t

def _fab_12(obj, nd):
	def t():
		_ciclo_drone(12, nd, obj)
	return t

def _fab_13(obj, nd):
	def t():
		_ciclo_drone(13, nd, obj)
	return t

def _fab_14(obj, nd):
	def t():
		_ciclo_drone(14, nd, obj)
	return t

def _fab_15(obj, nd):
	def t():
		_ciclo_drone(15, nd, obj)
	return t

def _fab_16(obj, nd):
	def t():
		_ciclo_drone(16, nd, obj)
	return t

def _fab_17(obj, nd):
	def t():
		_ciclo_drone(17, nd, obj)
	return t

def _fab_18(obj, nd):
	def t():
		_ciclo_drone(18, nd, obj)
	return t

def _fab_19(obj, nd):
	def t():
		_ciclo_drone(19, nd, obj)
	return t

def _fab_20(obj, nd):
	def t():
		_ciclo_drone(20, nd, obj)
	return t

def _fab_21(obj, nd):
	def t():
		_ciclo_drone(21, nd, obj)
	return t

def _fab_22(obj, nd):
	def t():
		_ciclo_drone(22, nd, obj)
	return t

def _fab_23(obj, nd):
	def t():
		_ciclo_drone(23, nd, obj)
	return t

def _fab_24(obj, nd):
	def t():
		_ciclo_drone(24, nd, obj)
	return t

def _fab_25(obj, nd):
	def t():
		_ciclo_drone(25, nd, obj)
	return t

def _fab_26(obj, nd):
	def t():
		_ciclo_drone(26, nd, obj)
	return t

def _fab_27(obj, nd):
	def t():
		_ciclo_drone(27, nd, obj)
	return t

def _fab_28(obj, nd):
	def t():
		_ciclo_drone(28, nd, obj)
	return t

def _fab_29(obj, nd):
	def t():
		_ciclo_drone(29, nd, obj)
	return t

def _fab_30(obj, nd):
	def t():
		_ciclo_drone(30, nd, obj)
	return t

def _fab_31(obj, nd):
	def t():
		_ciclo_drone(31, nd, obj)
	return t

_fabricas = [
	_fab_0,  _fab_1,  _fab_2,  _fab_3,
	_fab_4,  _fab_5,  _fab_6,  _fab_7,
	_fab_8,  _fab_9,  _fab_10, _fab_11,
	_fab_12, _fab_13, _fab_14, _fab_15,
	_fab_16, _fab_17, _fab_18, _fab_19,
	_fab_20, _fab_21, _fab_22, _fab_23,
	_fab_24, _fab_25, _fab_26, _fab_27,
	_fab_28, _fab_29, _fab_30, _fab_31
]

def _garante_weird_substance(nd):
	custo = _custo_labirinto()
	# cada drone precisa de 1 labirinto por ciclo
	necessario = custo * nd * 2
	if num_items(Items.Weird_Substance) < necessario:
		print("    [labirinto] abastecer Weird_Substance: " + str(necessario))
		import policultura
		policultura.cria_modo_policultura(Items.Weird_Substance, Entities.Tree)(necessario)

def _spawna_ciclo(objetivo):
	nd = max_drones()
	if nd < 1:
		nd = 1
	tam = get_world_size()
	cols, rows = _divisao_2d(tam, nd)

	drones = []
	i = 0
	while i < nd and i < len(_fabricas):
		tarefa = _fabricas[i](objetivo, nd)
		drone = spawn_drone(tarefa)
		if drone:
			drones.append(drone)
		else:
			tarefa()
		i += 1

	for drone in drones:
		wait_for(drone)

def modo_labirinto(objetivo):
	while num_items(Items.Gold) < objetivo:
		nd = max_drones()
		if nd < 1:
			nd = 1
		_garante_weird_substance(nd)
		tam = get_world_size()
		cols, rows = _divisao_2d(tam, nd)
		custo = _custo_labirinto()
		print("    [labirinto] gold=" + str(num_items(Items.Gold)) + "/" + str(objetivo) +
			" nd=" + str(nd) + " grade=" + str(cols) + "x" + str(rows) +
			" custo=" + str(custo))
		_spawna_ciclo(objetivo)
	clear()
	campo.ara()
