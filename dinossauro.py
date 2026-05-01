import campo
import chapeus
import gerenciador
import fila

_x_maca = 0
_y_maca = 0

def _atualiza_maca():
	global _x_maca
	global _y_maca
	resultado = measure()
	if resultado == None:
		return False
	_x_maca = resultado[0]
	_y_maca = resultado[1]
	return True

def _bfs_proximo_passo(x_atual, y_atual, x_alvo, y_alvo):
	# BFS para achar primeira direcao do caminho ate a maca
	visitados = set()
	visitados.add((x_atual, y_atual))
	q = fila.inicializa()

	for direcao in campo.direcoes:
		dx, dy = campo.deltas[direcao]
		nx = x_atual + dx
		ny = y_atual + dy
		# sem wrap - cobra nao pode atravessar borda com chapeu de dino
		if nx < 0 or nx >= campo.n or ny < 0 or ny >= campo.n:
			continue
		if (nx, ny) not in visitados:
			visitados.add((nx, ny))
			q["enfila"]((nx, ny, direcao))

	while not q["vazia"]():
		x, y, primeira = q["desenfila"]()
		if x == x_alvo and y == y_alvo:
			return primeira
		for direcao in campo.direcoes:
			dx, dy = campo.deltas[direcao]
			nx = x + dx
			ny = y + dy
			if nx < 0 or nx >= campo.n or ny < 0 or ny >= campo.n:
				continue
			if (nx, ny) not in visitados:
				visitados.add((nx, ny))
				q["enfila"]((nx, ny, primeira))

	return None

def _vai_para_maca():
	sem_progresso = [0]
	limite = campo.n * campo.n * 2

	while True:
		x_atual = get_pos_x()
		y_atual = get_pos_y()

		# chegou na maca atual - atualiza para proxima
		if x_atual == _x_maca and y_atual == _y_maca:
			if not _atualiza_maca():
				return  # sem proxima maca
			sem_progresso[0] = 0

		direcao = _bfs_proximo_passo(x_atual, y_atual, _x_maca, _y_maca)

		if direcao == None:
			return  # sem caminho = campo cheio ou bloqueado

		if not can_move(direcao):
			# direcao BFS bloqueada pela cauda - tenta qualquer direcao livre
			moveu = False
			for d in campo.direcoes:
				if can_move(d):
					move(d)
					moveu = True
					break
			if not moveu:
				return  # campo cheio
			sem_progresso[0] = sem_progresso[0] + 1
			if sem_progresso[0] > limite:
				return  # preso
		else:
			move(direcao)
			sem_progresso[0] = 0

def _serpentina():
	# fallback se measure() nao retornar maca
	direcao_h = East
	for lin in range(campo.n):
		for _ in range(campo.n - 1):
			if not move(direcao_h):
				return
		if lin < campo.n - 1:
			if not move(North):
				return
			direcao_h = West if direcao_h == East else East

def _ciclo_dino():
	campo.vai_para(0, 0)
	change_hat(Hats.Dinosaur_Hat)

	if _atualiza_maca():
		_vai_para_maca()
	else:
		_serpentina()

	chapeus.usa()

def modo_dinossauro(objetivo):
	while gerenciador.precisa(Items.Bone, objetivo):
		_ciclo_dino()
