import campo
import gerenciador
import megafazenda

def _till_ate_soil():
	while get_ground_type() != Grounds.Soil:
		till()

def _celula_vazia():
	return get_entity_type() == None

def _rega_celula():
	if num_items(Items.Water) > 0:
		use_item(Items.Water)

def _measure_safe(direcao=None):
	if direcao == None:
		val = measure()
	else:
		val = measure(direcao)
	if val == None:
		return 0
	return val

def _vizinho_maduro(direcao):
	val = measure(direcao)
	if val == None:
		return False
	return True

def _espera_crescer():
	pronto = False
	while not pronto:
		pronto = True
		for x in range(campo.n):
			for y in range(campo.n):
				campo.vai_para(x, y)
				_rega_celula()
				if not can_harvest():
					pronto = False

def _acao_limpa():
	def bloco():
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, _colhe_se_pronto)
	return bloco

def _colhe_se_pronto():
	if get_entity_type() != None and can_harvest():
		harvest()

def _limpa_campo():
	megafazenda.paraleliza_blocos(_acao_limpa())

def _ordena_coluna(col):
	trocou = True
	while trocou:
		trocou = False
		for j in range(campo.n - 1):
			campo.vai_para(col, j)
			if _vizinho_maduro(North) and _measure_safe() > _measure_safe(North):
				swap(North)
				trocou = True

def _ordena_linha(lin):
	trocou = True
	while trocou:
		trocou = False
		for j in range(campo.n - 1):
			campo.vai_para(j, lin)
			if _vizinho_maduro(East) and _measure_safe() > _measure_safe(East):
				swap(East)
				trocou = True

def _ordena_campo():
	for _ in range(campo.n):
		for col in range(campo.n):
			_ordena_coluna(col)
		for lin in range(campo.n):
			_ordena_linha(lin)

def _colhe_cactos_existentes():
	def acao():
		if get_entity_type() == Entities.Cactus and can_harvest():
			harvest()
	campo.movimento(acao)

def _planta_n(n_sementes):
	plantados = [0]
	def acao():
		if plantados[0] >= n_sementes:
			return
		if not _celula_vazia():
			if can_harvest():
				harvest()
			else:
				return
		if num_items(Items.Cactus) == 0:
			return
		_till_ate_soil()
		if num_unlocked(Unlocks.Plant):
			plant(Entities.Cactus)
			plantados[0] = plantados[0] + 1
		if num_items(Items.Water) > 0:
			use_item(Items.Water)
	campo.movimento(acao)

def _ciclo_com_n(n_celulas):
	_limpa_campo()
	_planta_n(n_celulas)
	_espera_crescer()
	_ordena_campo()
	campo.vai_para(0, 0)
	harvest()

def _reabastece_sementes():
	n_celulas = campo.n * campo.n
	_colhe_cactos_existentes()
	if num_items(Items.Cactus) == 0:
		print("    [erro] sem sementes de cacto - nao e possivel iniciar cultivo")
		return
	while num_items(Items.Cactus) < n_celulas:
		disponiveis = num_items(Items.Cactus)
		if disponiveis == 0:
			print("    [erro] sementes esgotaram durante reabastecimento")
			return
		print("    [cacto] reabastecendo: " + str(disponiveis) + " sementes")
		_ciclo_com_n(disponiveis)

def _planta_campo():
	def acao():
		if not _celula_vazia():
			if can_harvest():
				harvest()
			else:
				return
		_till_ate_soil()
		if num_unlocked(Unlocks.Plant) and num_items(Items.Cactus) > 0:
			plant(Entities.Cactus)
		if num_items(Items.Water) > 0:
			use_item(Items.Water)
	campo.movimento(acao)

def modo_cacto(objetivo):
	while gerenciador.precisa(Items.Cactus, objetivo):
		_reabastece_sementes()
		if num_items(Items.Cactus) == 0:
			print("    [cacto] sem sementes, abortando")
			return
		_limpa_campo()
		_planta_campo()
		_espera_crescer()
		_ordena_campo()
		campo.vai_para(0, 0)
		harvest()
