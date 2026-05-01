import campo

_hat_dino = [None]
_hat_normal = [None]

# custo em cactos para o jogo comprar 1 maca automaticamente
_CUSTO_MACA = 4

def configura_hats(hat_dino, hat_normal):
	_hat_dino[0] = hat_dino
	_hat_normal[0] = hat_normal

def _garante_hat_normal():
	if _hat_normal[0] != None:
		change_hat(_hat_normal[0])

def _garante_cactos():
	# o jogo compra 1 maca automaticamente ao equipar o chapeu de dino
	# se nao houver cactos suficientes, o change_hat falha com warning
	if num_items(Items.Cactus) >= _CUSTO_MACA:
		return
	print("    [dino] sem cactos para maca, farmando...")
	import cacto
	cacto.modo_cacto(_CUSTO_MACA * 4)

def _ciclo_dino():
	n = get_world_size()

	# garante hat normal ANTES de navegar (sem cauda bloqueando)
	_garante_hat_normal()

	# garante cactos para a maca automatica
	_garante_cactos()

	# posiciona no canto 0,0 com hat normal
	campo.vai_para(0, 0)

	# agora equipa o chapeu de dino (jogo compra maca com 4 cactos)
	if _hat_dino[0] != None:
		change_hat(_hat_dino[0])

	# serpentina com move() relativo
	# col 0: sobe North (y=0 -> y=n-1)
	# col 1: desce South (y=n-1 -> y=0)
	# entre colunas: move East
	col = 0
	while col < n:
		if col % 2 == 0:
			passos = 0
			while passos < n - 1:
				ok = move(North)
				if not ok:
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

	# serpentina completa - desequipa para colher cauda
	_garante_hat_normal()

def modo_dinossauro(objetivo):
	_garante_hat_normal()
	while num_items(Items.Bone) < objetivo:
		_ciclo_dino()
	_garante_hat_normal()
