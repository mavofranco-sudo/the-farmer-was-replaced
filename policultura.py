import campo
import gerenciador
import megafazenda

_fertilizante = False
_voto_por_casa = {}
_votos_pra_casa = {}
_plantas = [Entities.Grass, Entities.Bush, Entities.Tree, Entities.Carrot]

def cria_modo_policultura(recurso, planta):
	def funcao(objetivo):
		modo_policultura(recurso, planta, objetivo)

	return funcao

def cria_modo_policultura_com_reabastecimento(recurso, planta, reabastece):
	def funcao(objetivo):
		modo_policultura_com_reabastecimento(recurso, planta, objetivo, reabastece)

	return funcao

def decide_planta(x, y, planta):
	global _voto_por_casa
	global _votos_pra_casa

	if planta == Entities.Tree and x % 2 != y % 2:
		planta = Entities.Bush

	planta_vencedora = planta
	votos_vencedores = 0
	for candidata in _votos_pra_casa[(x, y)]:
		votos = _votos_pra_casa[(x, y)][candidata]
		if votos > votos_vencedores:
			planta_vencedora = candidata
			votos_vencedores = votos

	return planta_vencedora

def vota(x, y):
	global _voto_por_casa
	global _votos_pra_casa

	if not num_unlocked(Unlocks.Polyculture):
		return

	candidata, (x_candidata, y_candidata) = get_companion()

	# ignora se a candidata nao esta no dicionario de votos (ex: e a propria planta alvo)
	if candidata not in _votos_pra_casa[(x_candidata, y_candidata)]:
		return

	if _voto_por_casa[(x, y)]:
		candidata_anterior, x_candidata_anterior, y_candidata_anterior = _voto_por_casa[(x, y)]
		# desfaz voto anterior apenas se ainda e valido
		if candidata_anterior in _votos_pra_casa[(x_candidata_anterior, y_candidata_anterior)]:
			_votos_pra_casa[(x_candidata_anterior, y_candidata_anterior)][candidata_anterior] -= 1
	_voto_por_casa[(x, y)] = (candidata, x_candidata, y_candidata)
	_votos_pra_casa[(x_candidata, y_candidata)][candidata] += 1

def cultiva_e_vota(planta):
	def funcao():
		global _fertilizante

		x, y = get_pos_x(), get_pos_y()

		vencedora = decide_planta(x, y, planta)
		if vencedora == Entities.Carrot:
			campo.colhe_e_cultiva_arado(vencedora, _fertilizante)
		else:
			campo.colhe_e_cultiva(vencedora, _fertilizante)
		if vencedora == planta:
			vota(x, y)

	return funcao

def tarefa(planta):
	def funcao():
		campo.movimento_bloco(megafazenda.linhas, megafazenda.colunas, cultiva_e_vota(planta))

	return funcao

def inicializa_estado(recurso, planta):
	global _fertilizante
	global _voto_por_casa
	global _votos_pra_casa

	_fertilizante = recurso == Items.Weird_Substance
	for x in range(campo.n):
		for y in range(campo.n):
			_voto_por_casa[(x, y)] = None
			_votos_pra_casa[(x, y)] = {}
			for p in _plantas:
				if p == planta:
					continue
				_votos_pra_casa[(x, y)][p] = 0

def modo_policultura(recurso, planta, objetivo):
	inicializa_estado(recurso, planta)
	while gerenciador.precisa(recurso, objetivo):
		megafazenda.paraleliza_blocos(tarefa(planta))
	campo.limpa()

def modo_policultura_com_reabastecimento(recurso, planta, objetivo, reabastece):
	inicializa_estado(recurso, planta)
	while gerenciador.precisa(recurso, objetivo):
		reabastece()
		megafazenda.paraleliza_blocos(tarefa(planta))
	campo.limpa()
