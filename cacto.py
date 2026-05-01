import campo
import gerenciador
import megafazenda

def _till_ate_soil():
	while get_ground_type() != Grounds.Soil:
		till()

def _planta_cacto():
	_till_ate_soil()
	if num_unlocked(Unlocks.Plant):
		plant(Entities.Cactus)
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

def insertion_sort(direcao, planta=False):
	x, y = get_pos_x(), get_pos_y()

	if planta:
		_planta_cacto()

	for i in range(1, campo.n):
		x_proximo, y_proximo = campo.proximo(x, y, campo.opostos[direcao], i)
		campo.vai_para(x_proximo, y_proximo)
		if planta:
			_planta_cacto()

		j = i
		while j > 0 and _measure_safe(direcao) > _measure_safe():
			swap(direcao)
			move(direcao)
			j -= 1

def cria_insertion_sort(direcao, planta=False):
	def funcao():
		insertion_sort(direcao, planta)

	return funcao

def modo_cacto(objetivo):
	while gerenciador.precisa(Items.Cactus, objetivo):
		megafazenda.paraleliza_linha(cria_insertion_sort(West, True))
		megafazenda.paraleliza_linha(cria_insertion_sort(South, False))

		campo.vai_para(0, 0)
		harvest()
