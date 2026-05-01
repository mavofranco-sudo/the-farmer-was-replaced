import campo
import fila
import gerenciador
import megafazenda

_fila = None

# FASE 1: planta em todas as celulas (primeira vez)
def inicializa():
	global _fila

	campo.cultiva_arado(Entities.Pumpkin)
	_fila["enfila"]((get_pos_x(), get_pos_y()))

# FASE 2: percorre o campo checando mortas e nao prontas
# Retorna True se todas estao prontas pra colher (can_harvest)
def _verifica_celula(x, y):
	global _fila

	tipo = get_entity_type()
	if tipo == Entities.Dead_Pumpkin:
		# replanta em cima da morta (remove automaticamente)
		campo.cultiva_arado(Entities.Pumpkin)
		_fila["enfila"]((x, y))
	elif not can_harvest():
		# ainda crescendo, volta pra fila
		_fila["enfila"]((x, y))

def _aguarda_e_replanta():
	global _fila

	_fila = fila.inicializa()
	campo.movimento_linha(inicializa)

	# loop ate todas estarem prontas
	while not _fila["vazia"]():
		x, y = _fila["desenfila"]()
		campo.vai_para(x, y)
		_verifica_celula(x, y)

# FASE 3: colhe a mega abobora (uma unica harvest no campo inteiro)
def _colhe_mega():
	campo.movimento_linha(harvest)

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
	campo.ara()
	while gerenciador.precisa(Items.Pumpkin, objetivo):
		_reabastece()
		_aguarda_e_replanta()
		_colhe_mega()
		campo.ara()

