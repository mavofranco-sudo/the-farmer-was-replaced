import campo
import fila
import gerenciador
import megafazenda

_fila = None

def inicializa():
	global _fila

	campo.colhe_e_cultiva_arado(Entities.Pumpkin)
	_fila["enfila"]((get_pos_x(), get_pos_y()))

def verifica(x, y):
	global _fila

	if not can_harvest():
		_fila["enfila"]((x, y))

		if get_entity_type() == Entities.Dead_Pumpkin:
			campo.colhe_e_cultiva_arado(Entities.Pumpkin)

def tarefa():
	global _fila

	_fila = fila.inicializa()
	campo.movimento_linha(inicializa)

	while not _fila["vazia"]():
		x, y = _fila["desenfila"]()
		campo.vai_para(x, y)
		verifica(x, y)

def _reabastece():
	custo_por_semente = 512
	minimo_cenouras = custo_por_semente + 50
	custo_wood = minimo_cenouras * 2 + 50
	custo_hay = minimo_cenouras * 2 + 50
	if num_items(Items.Wood) < custo_wood:
		gerenciador.farma_recurso(Items.Wood, custo_wood)
	if num_items(Items.Hay) < custo_hay:
		gerenciador.farma_recurso(Items.Hay, custo_hay)
	if num_items(Items.Carrot) < minimo_cenouras:
		gerenciador.farma_recurso(Items.Carrot, minimo_cenouras)

def modo_abobora(objetivo):
	while gerenciador.precisa(Items.Pumpkin, objetivo):
		_reabastece()
		megafazenda.paraleliza_linha(tarefa)
		harvest()
