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
	campo.agua()

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
		while j > 0 and measure(direcao) > measure():
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
		megafazenda.paraleliza_linha(cria_insertion_sort(South), False)

		campo.vai_para(0, 0)
		harvest()
