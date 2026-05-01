import campo
import megafazenda
import chapeus

def _navega_para_tesouro(x_ini, y_ini):
	visitados = []
	visitados.append([x_ini, y_ini])
	pilha = [[x_ini, y_ini, 0, None]]

	while len(pilha) > 0:
		topo = pilha[len(pilha) - 1]
		x = topo[0]
		y = topo[1]
		idx = topo[2]
		volta = topo[3]

		if get_entity_type() == Entities.Treasure:
			return True

		if idx >= len(campo.direcoes):
			pilha.pop()
			if volta != None:
				move(volta)
			continue

		topo[2] = idx + 1
		direcao = campo.direcoes[idx]
		proximo = campo.proximo(x, y, direcao)
		x_p = proximo[0]
		y_p = proximo[1]

		ja_visitado = False
		for v in visitados:
			if v[0] == x_p and v[1] == y_p:
				ja_visitado = True
				break

		if ja_visitado:
			continue
		if not can_move(direcao):
			continue

		visitados.append([x_p, y_p])
		move(direcao)
		pilha.append([x_p, y_p, 0, campo.opostos[direcao]])

	return False

def _nivel_mazes():
	n = num_unlocked(Unlocks.Mazes)
	if n == 0:
		return 1
	return 2 ** (n - 1)

def _custo_entrada():
	tam = get_world_size()
	return _nivel_mazes() * tam

def _divisao_2d(n, nd):
	# divide nd drones em grade cols x rows mais quadrada possivel
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

def _centro_regiao(indice, nd):
	# calcula o centro da regiao do drone de indice dado
	tam = get_world_size()
	cols, rows = _divisao_2d(tam, nd)

	# largura e altura de cada regiao
	w = (tam + cols - 1) // cols
	h = (tam + rows - 1) // rows

	# qual coluna e linha da grade pertence a este indice
	# percorre: col 0 row 0, col 0 row 1, ..., col 0 row rows-1, col 1 row 0, ...
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
	return cx, cy

def _ciclo_drone(indice, nd, objetivo):
	custo = _custo_entrada()
	centro = _centro_regiao(indice, nd)
	cx = centro[0]
	cy = centro[1]

	campo.vai_para(cx, cy)
	campo.cultiva(Entities.Bush)

	for _ in range(301):
		if num_items(Items.Gold) >= objetivo:
			break
		if num_items(Items.Weird_Substance) < custo:
			break
		use_item(Items.Weird_Substance, custo)

		resultado = measure()
		if resultado == None:
			continue

		x = get_pos_x()
		y = get_pos_y()
		_navega_para_tesouro(x, y)

	if get_entity_type() != None and can_harvest():
		harvest()

# 32 fabricas para paraleliza_blocos - cada uma executa o ciclo do drone i
def _faz_drone_0(objetivo, nd):
	def t():
		_ciclo_drone(0, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_1(objetivo, nd):
	def t():
		_ciclo_drone(1, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_2(objetivo, nd):
	def t():
		_ciclo_drone(2, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_3(objetivo, nd):
	def t():
		_ciclo_drone(3, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_4(objetivo, nd):
	def t():
		_ciclo_drone(4, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_5(objetivo, nd):
	def t():
		_ciclo_drone(5, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_6(objetivo, nd):
	def t():
		_ciclo_drone(6, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_7(objetivo, nd):
	def t():
		_ciclo_drone(7, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_8(objetivo, nd):
	def t():
		_ciclo_drone(8, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_9(objetivo, nd):
	def t():
		_ciclo_drone(9, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_10(objetivo, nd):
	def t():
		_ciclo_drone(10, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_11(objetivo, nd):
	def t():
		_ciclo_drone(11, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_12(objetivo, nd):
	def t():
		_ciclo_drone(12, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_13(objetivo, nd):
	def t():
		_ciclo_drone(13, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_14(objetivo, nd):
	def t():
		_ciclo_drone(14, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_15(objetivo, nd):
	def t():
		_ciclo_drone(15, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_16(objetivo, nd):
	def t():
		_ciclo_drone(16, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_17(objetivo, nd):
	def t():
		_ciclo_drone(17, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_18(objetivo, nd):
	def t():
		_ciclo_drone(18, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_19(objetivo, nd):
	def t():
		_ciclo_drone(19, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_20(objetivo, nd):
	def t():
		_ciclo_drone(20, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_21(objetivo, nd):
	def t():
		_ciclo_drone(21, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_22(objetivo, nd):
	def t():
		_ciclo_drone(22, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_23(objetivo, nd):
	def t():
		_ciclo_drone(23, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_24(objetivo, nd):
	def t():
		_ciclo_drone(24, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_25(objetivo, nd):
	def t():
		_ciclo_drone(25, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_26(objetivo, nd):
	def t():
		_ciclo_drone(26, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_27(objetivo, nd):
	def t():
		_ciclo_drone(27, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_28(objetivo, nd):
	def t():
		_ciclo_drone(28, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_29(objetivo, nd):
	def t():
		_ciclo_drone(29, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_30(objetivo, nd):
	def t():
		_ciclo_drone(30, nd, objetivo)
	return chapeus.usa_e_faz(t)

def _faz_drone_31(objetivo, nd):
	def t():
		_ciclo_drone(31, nd, objetivo)
	return chapeus.usa_e_faz(t)

_fabricas = [
	_faz_drone_0,  _faz_drone_1,  _faz_drone_2,  _faz_drone_3,
	_faz_drone_4,  _faz_drone_5,  _faz_drone_6,  _faz_drone_7,
	_faz_drone_8,  _faz_drone_9,  _faz_drone_10, _faz_drone_11,
	_faz_drone_12, _faz_drone_13, _faz_drone_14, _faz_drone_15,
	_faz_drone_16, _faz_drone_17, _faz_drone_18, _faz_drone_19,
	_faz_drone_20, _faz_drone_21, _faz_drone_22, _faz_drone_23,
	_faz_drone_24, _faz_drone_25, _faz_drone_26, _faz_drone_27,
	_faz_drone_28, _faz_drone_29, _faz_drone_30, _faz_drone_31
]

def _garante_weird_substance(objetivo, nd):
	custo = _custo_entrada()
	# cada drone faz 301 uses por ciclo
	necessario = custo * 301 * nd * 2
	if num_items(Items.Weird_Substance) < necessario:
		print("    [labirinto] abastecer Weird_Substance: " + str(necessario))
		import policultura
		policultura.cria_modo_policultura(Items.Weird_Substance, Entities.Tree)(necessario)

def _spawna_drones(objetivo):
	nd = max_drones()
	if nd < 1:
		nd = 1
	tam = get_world_size()
	cols, rows = _divisao_2d(tam, nd)

	drones = []
	i = 0
	while i < nd and i < len(_fabricas):
		centro = _centro_regiao(i, nd)
		campo.vai_para(centro[0], centro[1])
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
		_garante_weird_substance(objetivo, nd)
		tam = get_world_size()
		cols, rows = _divisao_2d(tam, nd)
		print("    [labirinto] gold=" + str(num_items(Items.Gold)) + "/" + str(objetivo) +
			" nd=" + str(nd) + " grade=" + str(cols) + "x" + str(rows) +
			" custo=" + str(_custo_entrada()))
		_spawna_drones(objetivo)
	clear()
	campo.ara()
