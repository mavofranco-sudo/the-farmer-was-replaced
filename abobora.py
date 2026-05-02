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

def _planta_aqui():
	# helper: usa till_ate_soil do campo (loop ate Soil garantido)
	campo.till_ate_soil()
	if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
		if num_unlocked(Unlocks.Plant):
			plant(Entities.Pumpkin)

def _verifica_e_trata_celula():
	tipo = get_entity_type()
	# caso 1: celula vazia
	if tipo == None:
		_planta_aqui()
		_tem_problema[0] = True
		return
	# caso 2: abobora podre (Dead_Pumpkin)
	if tipo == Entities.Dead_Pumpkin:
		harvest()
		_planta_aqui()
		_tem_problema[0] = True
		return
	# caso 3: abobora viva madura - ok, nao faz nada
	if tipo == Entities.Pumpkin:
		if can_harvest():
			return
		# caso 3b: crescendo - rega e marca pendente (nao e problema estrutural)
		campo._agua()
		_tem_crescendo[0] = True
		return
	# caso 4: qualquer outra entidade estranha - colhe e replanta
	if can_harvest():
		harvest()
	_planta_aqui()
	_tem_problema[0] = True

def _colhe_celula_bonus():
	# colhe SOMENTE abobora madura para garantir bonus n² (colheita simultanea)
	tipo = get_entity_type()
	if tipo == Entities.Pumpkin:
		if can_harvest():
			harvest()

def _replanta_celula():
	tipo = get_entity_type()
	if tipo != None:
		if can_harvest():
			harvest()
	campo.till_ate_soil()
	if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
		if num_unlocked(Unlocks.Plant):
			plant(Entities.Pumpkin)

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

# flag separado para aboboras ainda crescendo
_tem_crescendo = [False]

def _verifica_maturidade():
	# aguarda maturidade: so rega se ainda crescendo, trata problemas se aparecerem
	tipo = get_entity_type()
	if tipo == None:
		_planta_aqui()
		_tem_problema[0] = True
		return
	if tipo == Entities.Dead_Pumpkin:
		harvest()
		_planta_aqui()
		_tem_problema[0] = True
		return
	if tipo == Entities.Pumpkin:
		if can_harvest():
			# madura: nao faz nada, nao rega (para nao interferir)
			return
		# ainda crescendo: rega para acelerar
		campo._agua()
		_tem_crescendo[0] = True
		return
	# entidade estranha: limpa e replanta
	if can_harvest():
		harvest()
	_planta_aqui()
	_tem_problema[0] = True

def _campo_sem_problemas():
	# passagem completa: trata problemas estruturais (mortas/vazias)
	# retorna True se nenhum problema estrutural foi encontrado
	_tem_problema[0] = False
	megafazenda.paraleliza_blocos(_verifica_e_trata_celula)
	return not _tem_problema[0]

def _campo_todo_maduro():
	# passagem completa: verifica se TODAS as aboboras estao maduras
	# nao trata nada, so rega as crescendo e marca flags
	_tem_problema[0] = False
	_tem_crescendo[0] = False
	megafazenda.paraleliza_blocos(_verifica_maturidade)
	# se achou problema estrutural OU crescendo, nao esta pronto
	if _tem_problema[0]:
		return False
	if _tem_crescendo[0]:
		return False
	return True

def modo_abobora(objetivo):
	campo.inicializa()
	megafazenda.inicializa()
	# limpa e ara o campo todo antes de comecar
	megafazenda.paraleliza_blocos(_limpa_nao_abobora)
	megafazenda.paraleliza_blocos(_ara_celula)
	ciclo = 0
	while num_items(Items.Pumpkin) < objetivo:
		ciclo += 1
		campo.inicializa()
		megafazenda.inicializa()
		print("    [abobora] ciclo=" + str(ciclo) + " n=" + str(get_world_size()) +
			" abob=" + str(num_items(Items.Pumpkin)) + "/" + str(objetivo))

		# reabastece insumos antes de cada ciclo
		_reabastece_insumos()

		# FASE 1: garante campo 100% plantado e sem mortas
		# repassa ate nenhum problema estrutural
		print("    [abobora] fase1: limpando e plantando...")
		while not _campo_sem_problemas():
			pass

		# FASE 2: aguarda todas as aboboras atingirem can_harvest
		# se aparecer morta/vazia durante espera volta para fase 1
		print("    [abobora] fase2: aguardando maturidade...")
		esperas = 0
		pronto = False
		while not pronto:
			if _campo_todo_maduro():
				pronto = True
			else:
				esperas += 1
				if _tem_problema[0]:
					# problema estrutural apareceu: trata antes de continuar
					while not _campo_sem_problemas():
						pass

		print("    [abobora] maduras apos " + str(esperas) + " repasses - colhendo...")

		# FASE 3: colheita simultanea com todos os drones (bonus n²)
		megafazenda.paraleliza_blocos(_colhe_celula_bonus)

		# FASE 4: replanta campo inteiro imediatamente apos colheita
		print("    [abobora] replantando campo...")
		megafazenda.paraleliza_blocos(_replanta_celula)
