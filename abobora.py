import campo
import fila
import gerenciador
import megafazenda

_fila = None

def inicializa():
	global _fila

	campo.cultiva_arado(Entities.Pumpkin)
	_fila["enfila"]((get_pos_x(), get_pos_y()))

def verifica(x, y):
	global _fila

	if not can_harvest():
		_fila["enfila"]((x, y))

		if get_entity_type() == Entities.Dead_Pumpkin:
			campo.cultiva_arado(Entities.Pumpkin)

def tarefa():
	global _fila

	_fila = fila.inicializa()
	campo.movimento_linha(inicializa)

	while not _fila["vazia"]():
		x, y = _fila["desenfila"]()
		campo.vai_para(x, y)
		verifica(x, y)

def _reabastece():
	buffer = campo.n * campo.n * 512 + 512
	if num_items(Items.Carrot) < buffer:
		gerenciador.farma_recurso(Items.Carrot, buffer)

def modo_abobora(objetivo):
	while gerenciador.precisa(Items.Pumpkin, objetivo):
		_reabastece()
		megafazenda.paraleliza_linha(tarefa)
		harvest()
