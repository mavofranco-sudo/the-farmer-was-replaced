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

def _todas_prontas():
	for i in range(get_world_size()):
		for j in range(get_world_size()):
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
	# reinicializa sempre que chamado para pegar campo atual
	campo.inicializa()
	megafazenda.inicializa()
	campo.ara()
	while num_items(Items.Pumpkin) < objetivo:
		# reinicializa no inicio de cada ciclo para detectar Expand
		campo.inicializa()
		megafazenda.inicializa()
		_reabastece_insumos()
		megafazenda.paraleliza_blocos(_tarefa_planta_e_cuida())
		while not _todas_prontas():
			megafazenda.paraleliza_blocos(_tarefa_planta_e_cuida())
		megafazenda.paraleliza_blocos(_tarefa_colhe_tudo())
		campo.ara()
