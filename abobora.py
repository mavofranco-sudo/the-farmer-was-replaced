import campo
import megafazenda
import policultura

_CUSTO_SEMENTE = 512

# flag mutavel compartilhada entre drones para verificacao paralela
_tem_problema = [False]

def _trata_celula():
	tipo = get_entity_type()
	if tipo == None:
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Pumpkin)
		campo._agua()
	elif tipo == Entities.Dead_Pumpkin:
		harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Pumpkin)
		campo._agua()
	elif tipo == Entities.Pumpkin:
		if not can_harvest():
			campo._agua()
	else:
		if can_harvest():
			harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Pumpkin)
		campo._agua()

def _colhe_e_replanta():
	tipo = get_entity_type()
	if tipo == Entities.Pumpkin and can_harvest():
		harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Pumpkin)
		campo._agua()
	elif tipo == Entities.Pumpkin:
		campo._agua()
	elif tipo == Entities.Dead_Pumpkin:
		harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Pumpkin)
		campo._agua()
	elif tipo == None:
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Pumpkin)
		campo._agua()
	else:
		if can_harvest():
			harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Pumpkin)
		campo._agua()

def _verifica_celula():
	# cada drone marca _tem_problema se achou celula nao pronta
	tipo = get_entity_type()
	if tipo == None:
		_tem_problema[0] = True
	elif tipo == Entities.Dead_Pumpkin:
		_tem_problema[0] = True
	elif tipo == Entities.Pumpkin and not can_harvest():
		_tem_problema[0] = True

def _limpa_nao_abobora():
	tipo = get_entity_type()
	if tipo == None:
		return
	if tipo == Entities.Pumpkin:
		return
	if can_harvest():
		harvest()

def _ara_celula():
	till()

def _todas_prontas_paralelo():
	# reseta flag e manda todos os drones verificar em paralelo
	_tem_problema[0] = False
	megafazenda.paraleliza_blocos(_verifica_celula)
	return not _tem_problema[0]

def _noop():
	pass

def _reabastece_insumos():
	n = get_world_size()
	n_celulas = n * n
	minimo_cenouras = _CUSTO_SEMENTE * n_celulas + n_celulas * 2 + 100
	margem = minimo_cenouras * 2 + 100

	if num_items(Items.Wood) < margem:
		if num_unlocked(Unlocks.Trees) > 0:
			policultura.cria_modo_policultura(Items.Wood, Entities.Tree)(margem)
		else:
			policultura.cria_modo_policultura(Items.Wood, Entities.Bush)(margem)

	if num_items(Items.Hay) < margem:
		policultura.cria_modo_policultura(Items.Hay, Entities.Grass)(margem)

	if num_items(Items.Carrot) < minimo_cenouras:
		policultura.cria_modo_policultura_com_reabastecimento(
			Items.Carrot, Entities.Carrot, _noop
		)(minimo_cenouras)

def modo_abobora(objetivo):
	campo.inicializa()
	megafazenda.inicializa()
	megafazenda.paraleliza_blocos(_limpa_nao_abobora)
	megafazenda.paraleliza_blocos(_ara_celula)
	ciclo = 0
	while num_items(Items.Pumpkin) < objetivo:
		ciclo += 1
		campo.inicializa()
		megafazenda.inicializa()
		print("    [abobora] ciclo=" + str(ciclo) + " n=" + str(get_world_size()) +
			" abob=" + str(num_items(Items.Pumpkin)) + "/" + str(objetivo))
		_reabastece_insumos()
		megafazenda.paraleliza_blocos(_limpa_nao_abobora)
		megafazenda.paraleliza_blocos(_trata_celula)
		esperas = 0
		while not _todas_prontas_paralelo():
			esperas += 1
			megafazenda.paraleliza_blocos(_trata_celula)
		print("    [abobora] pronto apos " + str(esperas) + " esperas")
		megafazenda.paraleliza_blocos(_colhe_e_replanta)
