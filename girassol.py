import campo
import gerenciador
import megafazenda

def _tarefa_plantio():
	def funcao():
		def planta_celula():
			tipo = get_entity_type()
			if tipo == None:
				campo.till_ate_soil()
				plant(Entities.Sunflower)
			elif tipo != Entities.Sunflower:
				if can_harvest():
					harvest()
				campo.till_ate_soil()
				plant(Entities.Sunflower)
			campo._agua()
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, planta_celula)
	return funcao

def _tarefa_espera():
	def funcao():
		def rega_se_precisa():
			if get_entity_type() == Entities.Sunflower:
				campo._agua()
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, rega_se_precisa)
	return funcao

def _campo_todo_crescido():
	for x in range(campo.n):
		for y in range(campo.n):
			campo.vai_para(x, y)
			if get_entity_type() == Entities.Sunflower and not can_harvest():
				return False
	return True

def _colhe_por_ordem():
	petalas = []
	for x in range(campo.n):
		for y in range(campo.n):
			campo.vai_para(x, y)
			if get_entity_type() == Entities.Sunflower and can_harvest():
				p = measure()
				if p == None:
					p = 7
				petalas.append([p, x, y])

	# insertion sort decrescente
	for i in range(1, len(petalas)):
		chave = petalas[i]
		j = i - 1
		while j >= 0 and petalas[j][0] < chave[0]:
			petalas[j + 1] = petalas[j]
			j -= 1
		petalas[j + 1] = chave

	# colhe maior primeiro para garantir bonus 8x
	for item in petalas:
		campo.vai_para(item[1], item[2])
		if get_entity_type() == Entities.Sunflower and can_harvest():
			harvest()

def modo_girassol(objetivo):
	while gerenciador.precisa(Items.Power, objetivo):
		megafazenda.paraleliza_blocos(_tarefa_plantio())
		while not _campo_todo_crescido():
			megafazenda.paraleliza_blocos(_tarefa_espera())
		_colhe_por_ordem()
