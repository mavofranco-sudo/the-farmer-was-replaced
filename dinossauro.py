import campo

_hat_dino = [None]
_hat_normal = [None]

def configura_hats(hat_dino, hat_normal):
	_hat_dino[0] = hat_dino
	_hat_normal[0] = hat_normal

def _gera_rota_hamiltoniana():
	# Gera caminho hamiltoniano em serpentina que cobre n*n celulas
	# sem nunca cruzar: sobe col 0, desce col 1, sobe col 2, ...
	# resultado: lista de [x, y] em ordem de visita
	n = get_world_size()
	rota = []
	for col in range(n):
		if col % 2 == 0:
			# sobe: y de 0 ate n-1
			for lin in range(n):
				rota.append([col, lin])
		else:
			# desce: y de n-1 ate 0
			for lin in range(n - 1, -1, -1):
				rota.append([col, lin])
	return rota

def _ciclo_dino():
	n = get_world_size()
	# posiciona no canto 0,0
	campo.vai_para(0, 0)

	if _hat_dino[0] != None:
		change_hat(_hat_dino[0])

	# percorre toda a rota hamiltoniana
	# como e serpentina sem cruzamentos, a cauda nunca bloqueia
	rota = _gera_rota_hamiltoniana()
	total = len(rota)

	# pula a primeira posicao (ja estamos em 0,0)
	i = 1
	while i < total:
		destino = rota[i]
		x_dest = destino[0]
		y_dest = destino[1]
		x_atual = get_pos_x()
		y_atual = get_pos_y()

		# calcula direcao para o proximo passo
		dx = x_dest - x_atual
		dy = y_dest - y_atual

		if dx == 1:
			ok = move(East)
		elif dx == -1:
			ok = move(West)
		elif dy == 1:
			ok = move(North)
		elif dy == -1:
			ok = move(South)
		else:
			# nao deveria acontecer na serpentina, mas por seguranca
			ok = True

		if not ok:
			# cauda bloqueou - nao pode mais crescer, encerra
			break

		i += 1

	# desequipa o chapeu para colher a cauda (recebe ossos = comprimento^2)
	if _hat_normal[0] != None:
		change_hat(_hat_normal[0])

def modo_dinossauro(objetivo):
	while num_items(Items.Bone) < objetivo:
		_ciclo_dino()
