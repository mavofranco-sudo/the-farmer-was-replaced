import abobora
import cacto
import campo
import dinossauro
import girassol
import labirinto
import megafazenda
import policultura
import util

_ordem = []
_recursos = {}

def nivel(conquista):
	n = num_unlocked(conquista)
	if n == 0:
		return 1
	return 2**(n - 1)

def completada(conquista):
	return not get_cost(conquista)

def producao_segura(valor):
	if valor <= 0:
		return 1
	return valor

def pode_produzir(recurso):
	if recurso == Items.Power:
		return num_unlocked(Unlocks.Sunflowers) > 0
	if recurso == Items.Bone:
		return num_unlocked(Unlocks.Dinosaurs) > 0
	if recurso == Items.Gold:
		return num_unlocked(Unlocks.Mazes) > 0
	if recurso == Items.Cactus:
		return num_unlocked(Unlocks.Cactus) > 0
	if recurso == Items.Pumpkin:
		return num_unlocked(Unlocks.Pumpkins) > 0
	if recurso == Items.Wood:
		return num_unlocked(Unlocks.Trees) > 0
	if recurso == Items.Weird_Substance:
		return num_unlocked(Unlocks.Trees) > 0
	if recurso == Items.Carrot:
		return num_unlocked(Unlocks.Carrots) > 0
	return True

def inicializa():
	global _ordem
	global _recursos

	dimensao = min(megafazenda.linhas, megafazenda.colunas)
	if dimensao <= 0:
		dimensao = 1

	_ordem = [Items.Power, Items.Bone, Items.Gold, Items.Weird_Substance, Items.Cactus, Items.Pumpkin, Items.Carrot, Items.Wood, Items.Hay]
	_recursos = {
		Items.Hay: {
			"planta": Entities.Grass,
			"cultivo": policultura.cria_modo_policultura(Items.Hay, Entities.Grass),
			"ciclo_inicio": True,
			"custo_ciclo": campo.n * campo.n,
			"custo_energia_ciclo": campo.n * campo.n,
			"producao_ciclo": producao_segura((nivel(Unlocks.Polyculture) + 1) * ((nivel(Unlocks.Grass) * campo.n * campo.n) // 2))
		},
		Items.Wood: {
			"planta": Entities.Tree,
			"cultivo": policultura.cria_modo_policultura(Items.Wood, Entities.Tree),
			"ciclo_inicio": True,
			"custo_ciclo": campo.n * campo.n,
			"custo_energia_ciclo": campo.n * campo.n,
			"producao_ciclo": producao_segura((nivel(Unlocks.Polyculture) + 1) * ((nivel(Unlocks.Trees) * 3 * campo.n * campo.n) // 2))
		},
		Items.Carrot: {
			"planta": Entities.Carrot,
			"cultivo": policultura.cria_modo_policultura(Items.Carrot, Entities.Carrot),
			"ciclo_inicio": True,
			"custo_ciclo": campo.n * campo.n,
			"custo_energia_ciclo": campo.n * campo.n,
			"producao_ciclo": producao_segura((nivel(Unlocks.Polyculture) + 1) * ((nivel(Unlocks.Carrots) * campo.n * campo.n) // 2))
		},
		Items.Pumpkin: {
			"planta": Entities.Pumpkin,
			"cultivo": abobora.modo_abobora,
			"ciclo_inicio": False,
			"custo_ciclo": 2 * campo.n * campo.n,
			"custo_energia_ciclo": campo.n * campo.n * campo.n + campo.n * campo.n,
			"producao_ciclo": producao_segura(nivel(Unlocks.Pumpkins) * campo.n * campo.n * min(campo.n, 6))
		},
		Items.Power: {
			"planta": Entities.Sunflower,
			"cultivo": girassol.modo_girassol,
			"ciclo_inicio": False,
			"custo_ciclo": campo.n * campo.n,
			"custo_energia_ciclo": campo.n * campo.n,
			"producao_ciclo": producao_segura((nivel(Unlocks.Sunflowers) * 5 * ((campo.n * campo.n) - 9) + 9) - (campo.n * campo.n))
		},
		Items.Cactus: {
			"planta": Entities.Cactus,
			"cultivo": cacto.modo_cacto,
			"ciclo_inicio": False,
			"custo_ciclo": campo.n * campo.n,
			"custo_energia_ciclo": (campo.n * campo.n * campo.n) + (campo.n * (campo.n * campo.n) // 2),
			"producao_ciclo": producao_segura(nivel(Unlocks.Cactus) * (campo.n * campo.n)**2)
		},
		Items.Weird_Substance: {
			"planta": Entities.Tree,
			"cultivo": policultura.cria_modo_policultura(Items.Weird_Substance, Entities.Tree),
			"ciclo_inicio": True,
			"custo_ciclo": campo.n * campo.n,
			"custo_energia_ciclo": campo.n * campo.n,
			"producao_ciclo": producao_segura((nivel(Unlocks.Polyculture) + 1) * ((nivel(Unlocks.Trees) * 3 * campo.n * campo.n) // 2))
		},
		Items.Gold: {
			"planta": Entities.Treasure,
			"cultivo": labirinto.modo_labirinto,
			"ciclo_inicio": False,
			"custo_ciclo": 301 * megafazenda.n_drones * dimensao,
			"custo_energia_ciclo": 301 * megafazenda.n_drones * ((dimensao * dimensao) // 2),
			"producao_ciclo": producao_segura(301 * nivel(Unlocks.Mazes) * megafazenda.n_drones * dimensao * dimensao)
		},
		Items.Bone: {
			"planta": Entities.Apple,
			"cultivo": dinossauro.modo_dinossauro,
			"ciclo_inicio": False,
			"custo_ciclo": campo.n * campo.n,
			"custo_energia_ciclo": 2 * campo.n * campo.n * campo.n,
			"producao_ciclo": producao_segura(nivel(Unlocks.Dinosaurs) * (campo.n * campo.n)**2)
		}
}

def precisa(recurso, objetivo):
	return num_items(recurso) < objetivo

def farma_recurso(recurso, objetivo):
	global _recursos
	if not precisa(recurso, objetivo):
		return
	if not pode_produzir(recurso):
		return
	dados = _recursos[recurso]
	dados["cultivo"](objetivo)

def farma_custo(custo):
	global _ordem
	for recurso in _ordem:
		if recurso not in custo:
			continue
		farma_recurso(recurso, custo[recurso])
