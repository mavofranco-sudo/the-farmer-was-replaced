import campo
import megafazenda

_CUSTO_SEMENTE = 64

def _limpa_celula():
	if get_entity_type() != None and can_harvest():
		harvest()

def _planta_cacto():
	if num_items(Items.Pumpkin) < _CUSTO_SEMENTE:
		return
	tipo = get_entity_type()
	if tipo != None:
		if can_harvest():
			harvest()
		else:
			return
	# garante soil antes de plantar
	campo.till_ate_soil()
	if num_unlocked(Unlocks.Plant):
		plant(Entities.Cactus)
	campo._agua()

def _rega_celula():
	campo._agua()

def _conta_cactos_no_campo():
	total = 0
	tam = get_world_size()
	for x in range(tam):
		for y in range(tam):
			campo.vai_para(x, y)
			if get_entity_type() == Entities.Cactus:
				total += 1
	return total

def _campo_todo_crescido():
	tem_algum = False
	tam = get_world_size()
	for x in range(tam):
		for y in range(tam):
			campo.vai_para(x, y)
			if get_entity_type() == Entities.Cactus:
				tem_algum = True
				if not can_harvest():
					return False
	return tem_algum

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
		tam = get_world_size()
		for j in range(tam - 1):
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
		tam = get_world_size()
		for j in range(tam - 1):
			campo.vai_para(j, lin)
			v_atual = _measure_safe()
			vizinho_existe = measure(East) != None
			if vizinho_existe and v_atual > _measure_safe(East):
				swap(East)
				trocou = True

def _ordena_campo():
	tam = get_world_size()
	for _ in range(tam):
		for col in range(tam):
			_ordena_coluna(col)
		for lin in range(tam):
			_ordena_linha(lin)

def _aboboras_para_campo_cheio():
	tam = get_world_size()
	return tam * tam * _CUSTO_SEMENTE

def modo_cacto(objetivo):
	while num_items(Items.Cactus) < objetivo:
		aboboras_necessarias = _aboboras_para_campo_cheio()
		if num_items(Items.Pumpkin) < aboboras_necessarias:
			print("    [cacto] precisa de " + str(aboboras_necessarias) + " aboboras, tem " + str(num_items(Items.Pumpkin)))
			import abobora
			abobora.modo_abobora(aboboras_necessarias)

		megafazenda.paraleliza_blocos(_limpa_celula)
		megafazenda.paraleliza_blocos(_planta_cacto)
		while not _campo_todo_crescido():
			megafazenda.paraleliza_blocos(_rega_celula)
		_ordena_campo()
		campo.vai_para(0, 0)
		harvest()
