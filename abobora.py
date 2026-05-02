import campo
import megafazenda
import policultura

_CUSTO_SEMENTE = 512

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

def _verifica_e_trata_celula():
	tipo = get_entity_type()
	if tipo == None:
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Pumpkin)
		campo._agua()
		_tem_problema[0] = True
		return
	if tipo == Entities.Dead_Pumpkin:
		harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Pumpkin)
		campo._agua()
		_tem_problema[0] = True
		return
	if tipo == Entities.Pumpkin:
		if can_harvest():
			# madura: ok
			return
		# crescendo: rega e marca
		campo._agua()
		_tem_problema[0] = True
		return
	# qualquer outra entidade: limpa e replanta
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Soil:
		till()
	if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
		if num_unlocked(Unlocks.Plant):
			plant(Entities.Pumpkin)
	campo._agua()
	_tem_problema[0] = True

def _so_colhe_madura():
	# colhe APENAS se for Pumpkin madura — nao toca em nada mais
	tipo = get_entity_type()
	if tipo == Entities.Pumpkin:
		if can_harvest():
			harvest()

def _replanta_celula():
	tipo = get_entity_type()
	if tipo != None:
		if can_harvest():
			harvest()
	if get_ground_type() != Grounds.Soil:
		till()
	if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
		if num_unlocked(Unlocks.Plant):
			plant(Entities.Pumpkin)
	campo._agua()

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

def _campo_sem_problemas():
	# uma passagem completa com todos os drones
	# retorna True SOMENTE se nenhum drone marcou problema
	_tem_problema[0] = False
	megafazenda.paraleliza_blocos(_verifica_e_trata_celula)
	return not _tem_problema[0]

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

		# loop: repassa ate 3 passagens limpas consecutivas sem nenhum problema
		esperas = 0
		limpas = 0
		while limpas < 3:
			if _campo_sem_problemas():
				limpas += 1
			else:
				limpas = 0
				esperas += 1

		print("    [abobora] campo ok apos " + str(esperas) + " repasses, colhendo...")

		# colheita: SO colhe Pumpkin madura, nao toca em nada mais
		megafazenda.paraleliza_blocos(_so_colhe_madura)

		# replanta para proximo ciclo
		megafazenda.paraleliza_blocos(_replanta_celula)
