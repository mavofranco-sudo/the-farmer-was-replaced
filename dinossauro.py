import campo
import gerenciador
import megafazenda
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
	visitados = set()
	visitados.add((x_atual, y_atual))
	q = fila.inicializa()

	for direcao in campo.direcoes:
		delta = campo.deltas[direcao]
		nx = x_atual + delta[0]
		ny = y_atual + delta[1]
		if nx < 0 or nx >= campo.n:
			continue
		if ny < 0 or ny >= campo.n:
			continue
		if (nx, ny) not in visitados:
			visitados.add((nx, ny))
			q["enfila"]([nx, ny, direcao])

	while not q["vazia"]():
		no = q["desenfila"]()
		x = no[0]
		y = no[1]
		primeira = no[2]
		if x == x_alvo and y == y_alvo:
			return primeira
		for direcao in campo.direcoes:
			delta = campo.deltas[direcao]
			nx = x + delta[0]
			ny = y + delta[1]
			if nx < 0 or nx >= campo.n:
				continue
			if ny < 0 or ny >= campo.n:
				continue
			if (nx, ny) not in visitados:
				visitados.add((nx, ny))
				q["enfila"]([nx, ny, primeira])

	return None

def _vai_para_maca():
	sem_progresso = [0]
	limite = campo.n * campo.n * 2

	while True:
		x_atual = get_pos_x()
		y_atual = get_pos_y()

		if x_atual == _x_maca and y_atual == _y_maca:
			if not _atualiza_maca():
				return
			sem_progresso[0] = 0

		direcao = _bfs_proximo_passo(x_atual, y_atual, _x_maca, _y_maca)

		if direcao == None:
			return

		if not can_move(direcao):
			moveu = False
			for d in campo.direcoes:
				if can_move(d):
					move(d)
					moveu = True
					break
			if not moveu:
				return
			sem_progresso[0] = sem_progresso[0] + 1
			if sem_progresso[0] > limite:
				return
		else:
			move(direcao)
			sem_progresso[0] = 0

def _serpentina():
	direcao_h = East
	for lin in range(campo.n):
		for _ in range(campo.n - 1):
			if not move(direcao_h):
				return
		if lin < campo.n - 1:
			if not move(North):
				return
			if direcao_h == East:
				direcao_h = West
			else:
				direcao_h = East

def _tarefa_dino():
	def funcao():
		campo.vai_para(get_pos_x(), get_pos_y())
		change_hat(Hats.Dinosaur_Hat)

		if _atualiza_maca():
			_vai_para_maca()
		else:
			_serpentina()

		change_hat(Hats.Straw_Hat)
	return funcao

def modo_dinossauro(objetivo):
	while gerenciador.precisa(Items.Bone, objetivo):
		megafazenda.paraleliza_blocos(_tarefa_dino())
