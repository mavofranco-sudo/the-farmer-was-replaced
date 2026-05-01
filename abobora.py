import campo
import megafazenda
import policultura

_CUSTO_SEMENTE = 512

def _tarefa_planta_e_cuida():
	def funcao():
		def trata_celula():
			tipo = get_entity_type()
			if tipo == None:
				if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
					campo.till_ate_soil()
					if num_unlocked(Unlocks.Plant):
						plant(Entities.Pumpkin)
				campo._agua()
			elif tipo == Entities.Dead_Pumpkin:
				harvest()
				if num_items(Items.Carrot) >= _CUSTO_SEMENTE:
					campo.till_ate_soil()
					if num_unlocked(Unlocks.Plant):
						plant(Entities.Pumpkin)
				campo._agua()
			elif tipo == Entities.Pumpkin:
				if not can_harvest():
					campo._agua()
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, trata_celula)
	return funcao

def _conta_campo():
	tam = get_world_size()
	total = 0
	prontas = 0
	vazias = 0
	mortas = 0
	crescendo = 0
	for i in range(tam):
		for j in range(tam):
			campo.vai_para(i, j)
			tipo = get_entity_type()
			total += 1
			if tipo == None:
				vazias += 1
			elif tipo == Entities.Dead_Pumpkin:
				mortas += 1
			elif tipo == Entities.Pumpkin:
				if can_harvest():
					prontas += 1
				else:
					crescendo += 1
	return [total, prontas, crescendo, mortas, vazias]

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

def _tarefa_colhe_tudo():
	def funcao():
		def colhe():
			if get_entity_type() == Entities.Pumpkin and can_harvest():
				harvest()
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, colhe)
	return funcao

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
	campo.ara()
	ciclo = 0
	while num_items(Items.Pumpkin) < objetivo:
		ciclo += 1
		campo.inicializa()
		megafazenda.inicializa()
		print("    [abobora] ciclo=" + str(ciclo) + " n=" + str(get_world_size()) +
			" bloco=" + str(megafazenda.colunas) + "x" + str(megafazenda.linhas) +
			" abob=" + str(num_items(Items.Pumpkin)) + "/" + str(objetivo))
		_reabastece_insumos()
		megafazenda.paraleliza_blocos(_tarefa_planta_e_cuida())
		contagem = _conta_campo()
		print("    [abobora] apos plantar: total=" + str(contagem[0]) +
			" prontas=" + str(contagem[1]) + " crescendo=" + str(contagem[2]) +
			" mortas=" + str(contagem[3]) + " vazias=" + str(contagem[4]))
		espera = 0
		while not _todas_prontas():
			espera += 1
			megafazenda.paraleliza_blocos(_tarefa_planta_e_cuida())
		print("    [abobora] campo pronto apos " + str(espera) + " esperas")
		megafazenda.paraleliza_blocos(_tarefa_colhe_tudo())
		campo.ara()
