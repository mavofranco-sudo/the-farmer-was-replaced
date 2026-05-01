import campo
import megafazenda
import policultura

_CUSTO_SEMENTE = 512

def _trata_celula():
	tipo = get_entity_type()
	if tipo == None:
		# verifica solo: so planta se for Soil, senao faz till primeiro
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

def _colhe_celula():
	if get_entity_type() == Entities.Pumpkin and can_harvest():
		harvest()

def _ara_celula():
	till()

def _todas_prontas():
	tam = get_world_size()
	for i in range(tam):
		for j in range(tam):
			campo.vai_para(i, j)
			tipo = get_entity_type()
			if tipo == None:
				return False
			if tipo == Entities.Dead_Pumpkin:
				return False
			if tipo == Entities.Pumpkin and not can_harvest():
				return False
	return True

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
	megafazenda.paraleliza_blocos(_ara_celula)
	ciclo = 0
	while num_items(Items.Pumpkin) < objetivo:
		ciclo += 1
		campo.inicializa()
		megafazenda.inicializa()
		print("    [abobora] ciclo=" + str(ciclo) + " n=" + str(get_world_size()) +
			" abob=" + str(num_items(Items.Pumpkin)) + "/" + str(objetivo))
		_reabastece_insumos()
		megafazenda.paraleliza_blocos(_trata_celula)
		esperas = 0
		while not _todas_prontas():
			esperas += 1
			megafazenda.paraleliza_blocos(_trata_celula)
		print("    [abobora] pronto apos " + str(esperas) + " esperas")
		megafazenda.paraleliza_blocos(_colhe_celula)
		megafazenda.paraleliza_blocos(_ara_celula)
