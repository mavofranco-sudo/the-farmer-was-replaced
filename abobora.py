import campo
import fila
import gerenciador
import megafazenda

_fila = None

def _till_ate_soil():
	while get_ground_type() != Grounds.Soil:
		till()

def _planta_abobora():
	_till_ate_soil()
	if num_unlocked(Unlocks.Plant):
		plant(Entities.Pumpkin)
	if num_items(Items.Water) > 0:
		use_item(Items.Water)

def inicializa():
	global _fila

	_planta_abobora()
	_fila["enfila"]((get_pos_x(), get_pos_y()))

def _verifica_celula(x, y):
	global _fila

	tipo = get_entity_type()
	if tipo == Entities.Dead_Pumpkin:
		_planta_abobora()
		_fila["enfila"]((x, y))
	elif not can_harvest():
		_fila["enfila"]((x, y))

def _aguarda_e_replanta():
	global _fila

	_fila = fila.inicializa()
	campo.movimento(inicializa)

	while not _fila["vazia"]():
		x, y = _fila["desenfila"]()
		campo.vai_para(x, y)
		_verifica_celula(x, y)

def _colhe_mega():
	campo.movimento(harvest)

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
		_aguarda_e_replanta()
		_colhe_mega()
		campo.ara()
