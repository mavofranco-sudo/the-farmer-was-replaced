import campo
import megafazenda

def _tarefa_limpa():
	def funcao():
		def colhe_se_pronto():
			if get_entity_type() != None and can_harvest():
				harvest()
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, colhe_se_pronto)
	return funcao

def _tarefa_planta():
	def funcao():
		def planta_cacto():
			if num_items(Items.Cactus) == 0:
				return
			tipo = get_entity_type()
			if tipo != None:
				if can_harvest():
					harvest()
				else:
					return
			campo.till_ate_soil()
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Cactus)
			campo._agua()
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, planta_cacto)
	return funcao

def _tarefa_espera():
	def funcao():
		def rega():
			campo._agua()
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, rega)
	return funcao

def _conta_cactos_no_campo():
	total = 0
	for x in range(campo.n):
		for y in range(campo.n):
			campo.vai_para(x, y)
			if get_entity_type() == Entities.Cactus:
				total += 1
	return total

def _campo_todo_crescido():
	# se nao tem cacto nenhum plantado, nao esta crescido
	tem_algum = False
	for x in range(campo.n):
		for y in range(campo.n):
			campo.vai_para(x, y)
			if get_entity_type() == Entities.Cactus:
				tem_algum = True
				if not can_harvest():
					return False
	return tem_algum

def _planta_primeiro_cacto():
	# planta pelo menos 1 cacto para ter semente para o resto
	# o jogo da a semente inicial quando o unlock e feito
	for x in range(campo.n):
		for y in range(campo.n):
			campo.vai_para(x, y)
			if get_entity_type() == None:
				campo.till_ate_soil()
				if num_unlocked(Unlocks.Plant):
					plant(Entities.Cactus)
				return

def _measure_safe(direcao=None):
	if direcao == None:
		val = measure()
	else:
		val = measure(direcao)
	if val == None:
		return 0
	return val

def _ordena_coluna(col):
	trocou = True
	while trocou:
		trocou = False
		for j in range(campo.n - 1):
			campo.vai_para(col, j)
			v_atual = _measure_safe()
			vizinho_existe = measure(North) != None
			if vizinho_existe and v_atual > _measure_safe(North):
				swap(North)
				trocou = True

def _ordena_linha(lin):
	trocou = True
	while trocou:
		trocou = False
		for j in range(campo.n - 1):
			campo.vai_para(j, lin)
			v_atual = _measure_safe()
			vizinho_existe = measure(East) != None
			if vizinho_existe and v_atual > _measure_safe(East):
				swap(East)
				trocou = True

def _ordena_campo():
	for _ in range(campo.n):
		for col in range(campo.n):
			_ordena_coluna(col)
		for lin in range(campo.n):
			_ordena_linha(lin)

def tem_cactos_suficientes():
	return num_items(Items.Cactus) >= campo.n * campo.n

def modo_cacto(objetivo):
	# garante que tem pelo menos 1 cacto no campo ou no inventario para comecar
	if num_items(Items.Cactus) == 0 and _conta_cactos_no_campo() == 0:
		_planta_primeiro_cacto()

	while num_items(Items.Cactus) < objetivo:
		megafazenda.paraleliza_blocos(_tarefa_limpa())
		megafazenda.paraleliza_blocos(_tarefa_planta())
		while not _campo_todo_crescido():
			megafazenda.paraleliza_blocos(_tarefa_espera())
		_ordena_campo()
		campo.vai_para(0, 0)
		harvest()
