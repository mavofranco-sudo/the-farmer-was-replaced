import campo

_hat_dino = [None]
_hat_normal = [None]

def configura_hats(hat_dino, hat_normal):
	_hat_dino[0] = hat_dino
	_hat_normal[0] = hat_normal

def _ciclo_dino():
	n = get_world_size()

	# posiciona no canto 0,0 ANTES de equipar o chapeu
	# (com chapeu de dino nao pode atravessar bordas)
	campo.vai_para(0, 0)

	if _hat_dino[0] != None:
		change_hat(_hat_dino[0])

	# serpentina com move() relativo - nunca usa vai_para com chapeu
	# col 0: sobe North (y=0 -> y=n-1)
	# col 1: desce South (y=n-1 -> y=0)
	# col 2: sobe North, etc.
	# entre colunas: move East
	col = 0
	while col < n:
		# percorre a coluna inteira (n-1 passos)
		if col % 2 == 0:
			# sobe
			passos = 0
			while passos < n - 1:
				ok = move(North)
				if not ok:
					# cauda preencheu tudo, acabou
					if _hat_normal[0] != None:
						change_hat(_hat_normal[0])
					return
				passos += 1
		else:
			# desce
			passos = 0
			while passos < n - 1:
				ok = move(South)
				if not ok:
					if _hat_normal[0] != None:
						change_hat(_hat_normal[0])
					return
				passos += 1

		# move para proxima coluna (exceto na ultima)
		col += 1
		if col < n:
			ok = move(East)
			if not ok:
				if _hat_normal[0] != None:
					change_hat(_hat_normal[0])
				return

	# desequipa para colher cauda (ossos = comprimento^2)
	if _hat_normal[0] != None:
		change_hat(_hat_normal[0])

def modo_dinossauro(objetivo):
	while num_items(Items.Bone) < objetivo:
		_ciclo_dino()
