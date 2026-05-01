import campo
import megafazenda

_dirs = [North, East, South, West]

def _vira_esquerda(idx):
	return (idx - 1) % 4

def _vira_direita(idx):
	return (idx + 1) % 4

def _vira_oposto(idx):
	return (idx + 2) % 4

def _custo_labirinto():
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

def _navega_ate_tesouro():
	direcao_idx = 0
	tam = get_world_size()
	limite = tam * tam * 4
	passos = 0
	while passos < limite:
		if get_entity_type() == Entities.Treasure:
			return True
		esq = _vira_esquerda(direcao_idx)
		if can_move(_dirs[esq]):
			direcao_idx = esq
			move(_dirs[direcao_idx])
			passos += 1
			continue
		if can_move(_dirs[direcao_idx]):
			move(_dirs[direcao_idx])
			passos += 1
			continue
		dir_idx = _vira_direita(direcao_idx)
		if can_move(_dirs[dir_idx]):
			direcao_idx = dir_idx
			move(_dirs[direcao_idx])
			passos += 1
			continue
		direcao_idx = _vira_oposto(direcao_idx)
		move(_dirs[direcao_idx])
		passos += 1
	return False

def _navega_drone(indice, nd):
	achou = _navega_ate_tesouro()
	if achou:
		harvest()
	else:
		if get_entity_type() != None and can_harvest():
			harvest()
	print("    [lab] drone=" + str(indice) + " achou=" + str(achou) + " gold=" + str(num_items(Items.Gold)))

def _garante_weird_substance(custo):
	if num_items(Items.Weird_Substance) >= custo:
		return
	print("    [labirinto] abastecer WS: " + str(custo) + " (tem " + str(num_items(Items.Weird_Substance)) + ")")
	import policultura
	policultura.cria_modo_policultura(Items.Weird_Substance, Entities.Tree)(custo)

def _abre_labirinto():
	custo = _custo_labirinto()
	tam = get_world_size()
	campo.vai_para(0, 0)
	if get_entity_type() != None:
		if can_harvest():
			harvest()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, custo)
	print("    [labirinto] aberto tam=" + str(tam) + " custo=" + str(custo))

def _fab_0(nd):
	def t():
		_navega_drone(0, nd)
	return t

def _fab_1(nd):
	def t():
		_navega_drone(1, nd)
	return t

def _fab_2(nd):
	def t():
		_navega_drone(2, nd)
	return t

def _fab_3(nd):
	def t():
		_navega_drone(3, nd)
	return t

def _fab_4(nd):
	def t():
		_navega_drone(4, nd)
	return t

def _fab_5(nd):
	def t():
		_navega_drone(5, nd)
	return t

def _fab_6(nd):
	def t():
		_navega_drone(6, nd)
	return t

def _fab_7(nd):
	def t():
		_navega_drone(7, nd)
	return t

def _fab_8(nd):
	def t():
		_navega_drone(8, nd)
	return t

def _fab_9(nd):
	def t():
		_navega_drone(9, nd)
	return t

def _fab_10(nd):
	def t():
		_navega_drone(10, nd)
	return t

def _fab_11(nd):
	def t():
		_navega_drone(11, nd)
	return t

def _fab_12(nd):
	def t():
		_navega_drone(12, nd)
	return t

def _fab_13(nd):
	def t():
		_navega_drone(13, nd)
	return t

def _fab_14(nd):
	def t():
		_navega_drone(14, nd)
	return t

def _fab_15(nd):
	def t():
		_navega_drone(15, nd)
	return t

def _fab_16(nd):
	def t():
		_navega_drone(16, nd)
	return t

def _fab_17(nd):
	def t():
		_navega_drone(17, nd)
	return t

def _fab_18(nd):
	def t():
		_navega_drone(18, nd)
	return t

def _fab_19(nd):
	def t():
		_navega_drone(19, nd)
	return t

def _fab_20(nd):
	def t():
		_navega_drone(20, nd)
	return t

def _fab_21(nd):
	def t():
		_navega_drone(21, nd)
	return t

def _fab_22(nd):
	def t():
		_navega_drone(22, nd)
	return t

def _fab_23(nd):
	def t():
		_navega_drone(23, nd)
	return t

def _fab_24(nd):
	def t():
		_navega_drone(24, nd)
	return t

def _fab_25(nd):
	def t():
		_navega_drone(25, nd)
	return t

def _fab_26(nd):
	def t():
		_navega_drone(26, nd)
	return t

def _fab_27(nd):
	def t():
		_navega_drone(27, nd)
	return t

def _fab_28(nd):
	def t():
		_navega_drone(28, nd)
	return t

def _fab_29(nd):
	def t():
		_navega_drone(29, nd)
	return t

def _fab_30(nd):
	def t():
		_navega_drone(30, nd)
	return t

def _fab_31(nd):
	def t():
		_navega_drone(31, nd)
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

def _ciclo_labirinto(nd):
	custo = _custo_labirinto()
	_garante_weird_substance(custo)
	_abre_labirinto()
	# drone 0 executa localmente, demais sao spawnados
	drones = []
	i = 1
	while i < nd and i < len(_fabricas):
		tarefa = _fabricas[i](nd)
		drone = spawn_drone(tarefa)
		if drone:
			drones.append(drone)
		else:
			tarefa()
		i += 1
	# drone local navega
	_navega_drone(0, nd)
	for drone in drones:
		wait_for(drone)

def modo_labirinto(objetivo):
	while num_items(Items.Gold) < objetivo:
		nd = max_drones()
		if nd < 1:
			nd = 1
		tam = get_world_size()
		custo = _custo_labirinto()
		print("    [labirinto] gold=" + str(num_items(Items.Gold)) + "/" + str(objetivo) +
			" nd=" + str(nd) + " tam=" + str(tam) + " custo_ws=" + str(custo))
		_ciclo_labirinto(nd)
	clear()
	campo.ara()
