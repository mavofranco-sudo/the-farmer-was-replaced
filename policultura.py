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

def _regenera_solo_paralelo():
	# fase 1: colhe tudo e planta Grass onde o solo eh Soil
	def _celula_fase1():
		if get_entity_type() != None and can_harvest():
			harvest()
		if get_ground_type() == Grounds.Soil:
			plant(Entities.Grass)
			campo._agua()
	megafazenda.paraleliza_blocos(_celula_fase1)

	# fase 2: aguarda e colhe a Grass plantada (repete ate nao ter nada pendente)
	pendente = [True]
	while pendente[0]:
		pendente[0] = False
		def _celula_fase2():
			tipo = get_entity_type()
			if tipo == None:
				return
			if can_harvest():
				harvest()
			else:
				campo._agua()
				pendente[0] = True
		megafazenda.paraleliza_blocos(_celula_fase2)

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

	if _precisa_de_soil(vencedora):
		if get_ground_type() != Grounds.Soil:
			till()
	# Grassland: nao faz till - se solo for Soil nao planta (campo foi regenerado antes)

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

def _precisa_grassland(planta):
	if planta == Entities.Grass:
		return True
	if planta == Entities.Bush:
		return True
	if planta == Entities.Tree:
		return True
	return False

def modo_policultura(recurso, planta, objetivo):
	# reinicializa dimensoes (campo pode ter expandido)
	campo.inicializa()
	megafazenda.inicializa()
	inicializa_estado(recurso, planta)
	# se planta precisa de Grassland, regenera solo antes com paralelismo
	if _precisa_grassland(planta):
		print("    [poli] regenerando solo para " + str(planta))
		_regenera_solo_paralelo()
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
	campo.inicializa()
	megafazenda.inicializa()
	inicializa_estado(recurso, planta)
	if _precisa_grassland(planta):
		print("    [poli] regenerando solo para " + str(planta))
		_regenera_solo_paralelo()
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
