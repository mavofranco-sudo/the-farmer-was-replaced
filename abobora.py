import campo
import gerenciador
import megafazenda

def _tarefa_planta_e_cuida():
	def funcao():
		def trata_celula():
			tipo = get_entity_type()
			if tipo == None:
				campo.till_ate_soil()
				if num_unlocked(Unlocks.Plant):
					plant(Entities.Pumpkin)
				campo._agua()
			elif tipo == Entities.Dead_Pumpkin:
				harvest()
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
	for x in range(campo.n):
		for y in range(campo.n):
			campo.vai_para(x, y)
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

def _reabastece():
	n_celulas = campo.n * campo.n
	custo_por_semente = 512
	margem = n_celulas * 2 + 100
	minimo_cenouras = custo_por_semente * n_celulas + margem
	custo_wood = minimo_cenouras * 2 + margem
	custo_hay = minimo_cenouras * 2 + margem
	if num_items(Items.Wood) < custo_wood:
		gerenciador.farma_recurso(Items.Wood, custo_wood)
	if num_items(Items.Hay) < custo_hay:
		gerenciador.farma_recurso(Items.Hay, custo_hay)
	if num_items(Items.Carrot) < minimo_cenouras:
		gerenciador.farma_recurso(Items.Carrot, minimo_cenouras)

def modo_abobora(objetivo):
	campo.ara()
	while gerenciador.precisa(Items.Pumpkin, objetivo):
		_reabastece()
		# planta o campo todo
		megafazenda.paraleliza_blocos(_tarefa_planta_e_cuida())
		# aguarda: rega e replanta podres, mas NAO colhe as boas
		while not _todas_prontas():
			megafazenda.paraleliza_blocos(_tarefa_planta_e_cuida())
		# so colhe quando TUDO estiver maduro - bonus mega-abobora
		megafazenda.paraleliza_blocos(_tarefa_colhe_tudo())
		campo.ara()
