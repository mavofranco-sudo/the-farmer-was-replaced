import campo
import gerenciador

def _planta_campo():
	for x in range(campo.n):
		for y in range(campo.n):
			campo.vai_para(x, y)
			if get_entity_type() == None:
				till()
				plant(Entities.Sunflower)
			elif get_entity_type() != Entities.Sunflower:
				if can_harvest():
					harvest()
				till()
				plant(Entities.Sunflower)

def _espera_crescer():
	pronto = False
	while not pronto:
		pronto = True
		for x in range(campo.n):
			for y in range(campo.n):
				campo.vai_para(x, y)
				if get_entity_type() == Entities.Sunflower and not can_harvest():
					pronto = False

def _colhe_por_ordem():
	# coleta petalas de cada celula
	petalas = []
	for x in range(campo.n):
		for y in range(campo.n):
			campo.vai_para(x, y)
			if get_entity_type() == Entities.Sunflower and can_harvest():
				p = measure()
				if p == None:
					p = 7
				petalas.append([p, x, y])

	# ordena decrescente por petalas (insertion sort)
	for i in range(1, len(petalas)):
		chave = petalas[i]
		j = i - 1
		while j >= 0 and petalas[j][0] < chave[0]:
			petalas[j + 1] = petalas[j]
			j -= 1
		petalas[j + 1] = chave

	# colhe na ordem certa (maior primeiro)
	for item in petalas:
		x = item[1]
		y = item[2]
		campo.vai_para(x, y)
		if get_entity_type() == Entities.Sunflower and can_harvest():
			harvest()

def modo_girassol(objetivo):
	while gerenciador.precisa(Items.Power, objetivo):
		_planta_campo()
		_espera_crescer()
		_colhe_por_ordem()
