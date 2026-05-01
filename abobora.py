import campo
import gerenciador
import megafazenda

def _tarefa_planta():
	def funcao():
		def planta_celula():
			tipo = get_entity_type()
			if tipo == Entities.Dead_Pumpkin or tipo == None:
				campo.colhe_e_cultiva_arado(Entities.Pumpkin)
			elif tipo == Entities.Pumpkin:
				if can_harvest():
					harvest()
					campo.cultiva_arado(Entities.Pumpkin)
				else:
					campo._agua()
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, planta_celula)
	return funcao

def _tarefa_espera():
	def funcao():
		def aguarda_e_rega():
			if get_entity_type() == Entities.Pumpkin and not can_harvest():
				campo._agua()
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, aguarda_e_rega)
	return funcao

def _tarefa_colhe():
	def funcao():
		def colhe_se_pronto():
			if get_entity_type() == Entities.Pumpkin and can_harvest():
				harvest()
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, colhe_se_pronto)
	return funcao

def _campo_todo_crescido():
	for x in range(campo.n):
		for y in range(campo.n):
			campo.vai_para(x, y)
			tipo = get_entity_type()
			if tipo == Entities.Pumpkin and not can_harvest():
				return False
			if tipo == Entities.Dead_Pumpkin:
				return False
	return True

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
		megafazenda.paraleliza_blocos(_tarefa_planta())
		while not _campo_todo_crescido():
			megafazenda.paraleliza_blocos(_tarefa_espera())
		megafazenda.paraleliza_blocos(_tarefa_colhe())
		campo.ara()
