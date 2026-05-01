import campo
import cacto

_hat_dino = [None]
_hat_normal = [None]

_CUSTO_MACA = 4

def configura_hats(hat_dino, hat_normal):
	_hat_dino[0] = hat_dino
	_hat_normal[0] = hat_normal

def _garante_hat_normal():
	if _hat_normal[0] != None:
		change_hat(_hat_normal[0])

def _garante_cactos_ciclo():
	n = get_world_size()
	buffer = n * n * _CUSTO_MACA
	if num_items(Items.Cactus) >= buffer:
		return
	print("    [dino] farmando cactos (buffer=" + str(buffer) + " tem=" + str(num_items(Items.Cactus)) + ")")
	cacto.modo_cacto(buffer)

def _limpa_celula_atual():
	# garante que a celula atual esta vazia para a maca ser colocada
	tipo = get_entity_type()
	if tipo == None:
		return
	if can_harvest():
		harvest()
	else:
		# se nao pode colher agora, forca (ex: cacto imaturo - nao deve existir mas por seguranca)
		harvest()

def _ciclo_dino():
	n = get_world_size()

	# 1. hat normal para navegar livremente
	_garante_hat_normal()

	# 2. cactos suficientes para o ciclo inteiro
	_garante_cactos_ciclo()

	# 3. vai para (0,0) com hat normal e limpa a celula
	campo.vai_para(0, 0)
	_limpa_celula_atual()

	# 4. equipa chapeu de dino
	# o jogo coloca a maca embaixo do drone consumindo 4 cactos
	# a celula DEVE estar vazia para a maca aparecer
	if _hat_dino[0] != None:
		change_hat(_hat_dino[0])

	# verifica se a maca apareceu (entidade deve ser Apple em (0,0))
	# se nao apareceu (sem cactos suficientes), aborta
	if get_entity_type() == None:
		print("    [dino] AVISO: maca nao apareceu em (0,0), abortando ciclo")
		_garante_hat_normal()
		return

	# 5. serpentina Hamiltonian: percorre todas as n² celulas sem repetir
	# col 0: sobe North (y=0 ate y=n-1)
	# col 1: desce South (y=n-1 ate y=0)
	# entre colunas: move East
	moves_feitos = 0

	col = 0
	while col < n:
		if col % 2 == 0:
			passos = 0
			while passos < n - 1:
				ok = move(North)
				if not ok:
					_garante_hat_normal()
					print("    [dino] ciclo encerrado col=" + str(col) + " moves=" + str(moves_feitos))
					return
				moves_feitos += 1
				passos += 1
		else:
			passos = 0
			while passos < n - 1:
				ok = move(South)
				if not ok:
					_garante_hat_normal()
					print("    [dino] ciclo encerrado col=" + str(col) + " moves=" + str(moves_feitos))
					return
				moves_feitos += 1
				passos += 1

		col += 1
		if col < n:
			ok = move(East)
			if not ok:
				_garante_hat_normal()
				print("    [dino] ciclo encerrado (East) col=" + str(col) + " moves=" + str(moves_feitos))
				return
			moves_feitos += 1

	# completou a serpentina inteira
	_garante_hat_normal()
	print("    [dino] ciclo COMPLETO moves=" + str(moves_feitos) + "/" + str(n * n - 1))

def modo_dinossauro(objetivo):
	_garante_hat_normal()
	while num_items(Items.Bone) < objetivo:
		_ciclo_dino()
		print("    [dino] bone=" + str(num_items(Items.Bone)) + "/" + str(objetivo) +
			" cactos=" + str(num_items(Items.Cactus)))
	_garante_hat_normal()
