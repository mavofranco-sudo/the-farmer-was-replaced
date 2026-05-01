import campo

_hat_dino = [None]
_hat_normal = [None]

def configura_hats(hat_dino, hat_normal):
	_hat_dino[0] = hat_dino
	_hat_normal[0] = hat_normal

def _garante_hat_normal():
	# garante que o hat normal esta equipado antes de se mover livremente
	if _hat_normal[0] != None:
		change_hat(_hat_normal[0])

def _ciclo_dino():
	n = get_world_size()

	# garante hat normal ANTES de navegar para (0,0)
	# sem isso, a cauda do ciclo anterior bloqueia o caminho
	_garante_hat_normal()

	# posiciona no canto 0,0 com hat normal (sem cauda bloqueando)
	campo.vai_para(0, 0)

	# so agora equipa o chapeu de dino
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
	# garante hat normal ao entrar (pode ter ficado com dino do ciclo anterior)
	_garante_hat_normal()
	while num_items(Items.Bone) < objetivo:
		_ciclo_dino()
	# garante hat normal ao sair
	_garante_hat_normal()
