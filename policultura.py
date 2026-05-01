import campo
import gerenciador
import megafazenda

_fertilizante = False
_voto_por_casa = {}
_votos_pra_casa = {}
_plantas = [Entities.Grass, Entities.Bush, Entities.Tree, Entities.Carrot]
_sem_consumivel = [Entities.Grass, Entities.Bush]

# plantas que precisam de Soil (till antes de plantar)
_precisa_soil = [Entities.Carrot, Entities.Pumpkin, Entities.Sunflower, Entities.Cactus]

# plantas que precisam de Grassland (NAO pode fazer till)
_precisa_grassland = [Entities.Grass, Entities.Bush, Entities.Tree]

def cria_modo_policultura(recurso, planta):
	def funcao(objetivo):
		modo_policultura(recurso, planta, objetivo)
	return funcao

def cria_modo_policultura_com_reabastecimento(recurso, planta, reabastece):
	def funcao(objetivo):
		modo_policultura_com_reabastecimento(recurso, planta, objetivo, reabastece)
	return funcao

def decide_planta(x, y, planta):
	if planta == Entities.Tree and x % 2 != y % 2:
		planta = Entities.Bush

	planta_vencedora = planta
	votos_vencedores = 0
	for candidata in _votos_pra_casa[(x, y)]:
		votos = _votos_pra_casa[(x, y)][candidata]
		if votos > votos_vencedores:
			planta_vencedora = candidata
			votos_vencedores = votos

	return planta_vencedora

def vota(x, y):
	if not num_unlocked(Unlocks.Polyculture):
		return
	resultado = get_companion()
	if resultado == None:
		return
	candidata = resultado[0]
	pos = resultado[1]
	x_candidata = pos[0]
	y_candidata = pos[1]

	if candidata not in _votos_pra_casa[(x_candidata, y_candidata)]:
		return

	voto_anterior = _voto_por_casa[(x, y)]
	if voto_anterior != None:
		candidata_anterior = voto_anterior[0]
		x_candidata_anterior = voto_anterior[1]
		y_candidata_anterior = voto_anterior[2]
		if candidata_anterior in _votos_pra_casa[(x_candidata_anterior, y_candidata_anterior)]:
			_votos_pra_casa[(x_candidata_anterior, y_candidata_anterior)][candidata_anterior] -= 1
	_voto_por_casa[(x, y)] = [candidata, x_candidata, y_candidata]
	_votos_pra_casa[(x_candidata, y_candidata)][candidata] += 1

def _precisa_de_soil(planta):
	for p in _precisa_soil:
		if p == planta:
			return True
	return False

def _precisa_de_grassland(planta):
	for p in _precisa_grassland:
		if p == planta:
			return True
	return False

def _prepara_solo(vencedora):
	# prepara o solo correto para a planta
	solo_atual = get_ground_type()
	if _precisa_de_soil(vencedora):
		# precisa de Soil - faz till se estiver em Grassland
		if solo_atual != Grounds.Soil:
			till()
	elif _precisa_de_grassland(vencedora):
		# precisa de Grassland - NAO faz till
		# se ja estiver em Soil, nao tem como reverter - tenta plantar mesmo assim
		pass

def _cultiva_celula(planta):
	global _fertilizante
	x = get_pos_x()
	y = get_pos_y()
	vencedora = decide_planta(x, y, planta)
	usa_consumivel = _fertilizante and vencedora not in _sem_consumivel

	tipo_atual = get_entity_type()
	if tipo_atual != None:
		if can_harvest():
			harvest()
		else:
			campo._agua()
			return

	# prepara solo correto para a planta escolhida
	_prepara_solo(vencedora)

	if num_unlocked(Unlocks.Plant):
		plant(vencedora)

	campo._agua()
	if usa_consumivel:
		campo._fertiliza()

	if vencedora == planta:
		vota(x, y)

def cultiva_e_vota(planta):
	def funcao():
		_cultiva_celula(planta)
	return funcao

def inicializa_estado(recurso, planta):
	global _fertilizante
	global _voto_por_casa
	global _votos_pra_casa

	_fertilizante = recurso == Items.Weird_Substance
	tam = get_world_size()
	for x in range(tam):
		for y in range(tam):
			_voto_por_casa[(x, y)] = None
			_votos_pra_casa[(x, y)] = {}
			for p in _plantas:
				if p == planta:
					continue
				_votos_pra_casa[(x, y)][p] = 0

def modo_policultura(recurso, planta, objetivo):
	inicializa_estado(recurso, planta)
	ciclo = 0
	while gerenciador.precisa(recurso, objetivo):
		ciclo += 1
		antes = num_items(recurso)
		megafazenda.paraleliza_blocos(cultiva_e_vota(planta))
		depois = num_items(recurso)
		if ciclo % 10 == 1:
			print("    [poli] " + str(recurso) + " ciclo=" + str(ciclo) +
				" antes=" + str(antes) + " depois=" + str(depois) +
				" obj=" + str(objetivo))
	campo.limpa()

def modo_policultura_com_reabastecimento(recurso, planta, objetivo, reabastece):
	inicializa_estado(recurso, planta)
	ciclo = 0
	while gerenciador.precisa(recurso, objetivo):
		ciclo += 1
		antes = num_items(recurso)
		reabastece()
		megafazenda.paraleliza_blocos(cultiva_e_vota(planta))
		depois = num_items(recurso)
		if ciclo % 10 == 1:
			print("    [poli] " + str(recurso) + " ciclo=" + str(ciclo) +
				" antes=" + str(antes) + " depois=" + str(depois) +
				" obj=" + str(objetivo))
	campo.limpa()
