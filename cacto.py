import campo
import gerenciador
import megafazenda

def _till_ate_soil():
	while get_ground_type() != Grounds.Soil:
		till()

def _celula_vazia():
	return get_entity_type() == None

def _planta_cacto():
	if not _celula_vazia():
		harvest()
	_till_ate_soil()
	if num_unlocked(Unlocks.Plant):
		plant(Entities.Cactus)
	if num_items(Items.Water) > 0:
		use_item(Items.Water)

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

def _limpa_campo():
	def acao():
		if get_entity_type() != None:
			if can_harvest():
				harvest()
	campo.movimento(acao)

def _planta_campo():
	def acao():
		_planta_cacto()
	campo.movimento(acao)

def _ciclo_cacto():
	# planta o que der com as sementes disponiveis
	def acao():
		if _celula_vazia() and num_items(Items.Cactus) > 0:
			_till_ate_soil()
			if num_unlocked(Unlocks.Plant):
				plant(Entities.Cactus)
			if num_items(Items.Water) > 0:
				use_item(Items.Water)
	campo.movimento(acao)
	_espera_crescer()
	_ordena_campo()
	campo.vai_para(0, 0)
	harvest()

def _reabastece_sementes():
	# precisa de n*n sementes para plantar o campo todo
	minimo = campo.n * campo.n + 10
	tentativas = 0
	while num_items(Items.Cactus) < minimo and tentativas < 10:
		tentativas = tentativas + 1
		_limpa_campo()
		_ciclo_cacto()

def modo_cacto(objetivo):
	while gerenciador.precisa(Items.Cactus, objetivo):
		_reabastece_sementes()
		_limpa_campo()
		_planta_campo()
		_espera_crescer()
		_ordena_campo()
		campo.vai_para(0, 0)
		harvest()
