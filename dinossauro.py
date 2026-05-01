import campo
import cacto

_hat_dino = [None]
_hat_normal = [None]

# custo em cactos por maca (o jogo compra automaticamente ao equipar o chapeu)
_CUSTO_MACA = 4

def configura_hats(hat_dino, hat_normal):
	_hat_dino[0] = hat_dino
	_hat_normal[0] = hat_normal

def _garante_hat_normal():
	if _hat_normal[0] != None:
		change_hat(_hat_normal[0])

def _garante_cactos_ciclo():
	# num de cactos para um ciclo completo: n² passos, cada passo pode precisar de maca
	# na pratica a maca fica ate morrer (colidir), entao o pior caso e n² macas = n²*4 cactos
	# usamos n² como buffer generoso
	n = get_world_size()
	buffer = n * n * _CUSTO_MACA
	if num_items(Items.Cactus) >= buffer:
		return
	print("    [dino] farmando cactos para buffer de " + str(buffer) + " (tem " + str(num_items(Items.Cactus)) + ")")
	cacto.modo_cacto(buffer)

def _ciclo_dino():
	n = get_world_size()

	# 1. garante hat normal para navegar livremente
	_garante_hat_normal()

	# 2. garante cactos suficientes para o ciclo inteiro ANTES de comecar
	_garante_cactos_ciclo()

	# 3. posiciona no canto (0,0) com hat normal (sem cauda bloqueando)
	campo.vai_para(0, 0)

	# 4. so agora equipa o chapeu de dino (jogo compra maca com 4 cactos)
	if _hat_dino[0] != None:
		change_hat(_hat_dino[0])

	# 5. serpentina com move() relativo - nunca vai_para com chapeu de dino
	# col 0: sobe North (y=0 -> y=n-1)
	# col 1: desce South (y=n-1 -> y=0), etc.
	# entre colunas: move East
	col = 0
	while col < n:
		if col % 2 == 0:
			passos = 0
			while passos < n - 1:
				ok = move(North)
				if not ok:
					# cauda preencheu o caminho - ciclo completo
					_garante_hat_normal()
					return
				passos += 1
		else:
			passos = 0
			while passos < n - 1:
				ok = move(South)
				if not ok:
					_garante_hat_normal()
					return
				passos += 1

		col += 1
		if col < n:
			ok = move(East)
			if not ok:
				_garante_hat_normal()
				return

	# serpentina completa - desequipa para liberar cauda (ossos = comprimento)
	_garante_hat_normal()

def modo_dinossauro(objetivo):
	_garante_hat_normal()
	while num_items(Items.Bone) < objetivo:
		_ciclo_dino()
		print("    [dino] bone=" + str(num_items(Items.Bone)) + "/" + str(objetivo) +
			" cactos=" + str(num_items(Items.Cactus)))
	_garante_hat_normal()
