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

def _colhe_se_pronto():
	if get_entity_type() != None and can_harvest():
		harvest()

def _limpa_campo():
	def bloco():
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, _colhe_se_pronto)
	megafazenda.paraleliza_blocos(bloco)

def _planta_cacto():
	if not _celula_vazia():
		if can_harvest():
			harvest()
		else:
			return
	_till_ate_soil()
	if num_unlocked(Unlocks.Plant):
		plant(Entities.Cactus)
	if num_items(Items.Water) > 0:
		use_item(Items.Water)

def _planta_campo():
	def acao():
		_planta_cacto()
	campo.movimento(acao)

def modo_cacto(objetivo):
	while gerenciador.precisa(Items.Cactus, objetivo):
		_limpa_campo()
		_planta_campo()
		_espera_crescer()
		_ordena_campo()
		campo.vai_para(0, 0)
		harvest()
