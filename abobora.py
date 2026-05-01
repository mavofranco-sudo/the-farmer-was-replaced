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

def _colhe_celula_madura():
	# fase 1: colhe APENAS aboboras maduras (garante bonus de colheita simultanea)
	tipo = get_entity_type()
	if tipo == Entities.Pumpkin and can_harvest():
		harvest()
	elif tipo == Entities.Dead_Pumpkin:
		harvest()
	elif tipo != None and tipo != Entities.Pumpkin:
		if can_harvest():
			harvest()

def _replanta_celula():
	# fase 2: ara e replanta tudo (campo deve estar limpo apos _colhe_celula_madura)
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

def _verifica_e_trata_celula():
	# cada drone: se achou problema ja resolve e marca flag para novo repasse
	tipo = get_entity_type()
	if tipo == None:
		# celula vazia: ara e replanta
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Pumpkin)
		campo._agua()
		_tem_problema[0] = True
	elif tipo == Entities.Dead_Pumpkin:
		# abobora morta: colhe, ara e replanta
		harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Pumpkin)
		campo._agua()
		_tem_problema[0] = True
	elif tipo == Entities.Pumpkin and not can_harvest():
		# abobora crescendo: rega e marca que ainda nao esta pronta
		campo._agua()
		_tem_problema[0] = True
	elif tipo == Entities.Pumpkin and can_harvest():
		# abobora madura: ok, nao marca problema
		pass
	else:
		# entidade estranha: limpa e replanta
		if can_harvest():
			harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Pumpkin)
		campo._agua()
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
	# reseta flag e manda todos os drones verificar+tratar em paralelo
	# se qualquer drone achou e corrigiu um problema, retorna False (precisa repassar)
	_tem_problema[0] = False
	megafazenda.paraleliza_blocos(_verifica_e_trata_celula)
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
		# repasses: verifica+trata ate campo estar ok
		# exige 2 confirmacoes consecutivas antes de colher (evita falso positivo)
		esperas = 0
		confirmacoes = 0
		while confirmacoes < 2:
			if _todas_prontas_paralelo():
				confirmacoes += 1
			else:
				confirmacoes = 0
				esperas += 1
		print("    [abobora] pronto apos " + str(esperas) + " repasses, colhendo...")
		# fase colheita: todos os drones colhem simultaneamente (garante bonus n²)
		megafazenda.paraleliza_blocos(_colhe_celula_madura)
		# fase replantio: ara e replanta (inclusive celulas que ficaram vazias)
		megafazenda.paraleliza_blocos(_replanta_celula)
