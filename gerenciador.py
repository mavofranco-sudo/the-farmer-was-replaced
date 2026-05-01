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
	if recurso == Items.Weird_Substance:
		return num_unlocked(Unlocks.Trees) > 0
	return True

def _cultivo_wood(objetivo):
	if num_unlocked(Unlocks.Trees) == 0:
		policultura.cria_modo_policultura(Items.Wood, Entities.Bush)(objetivo)
	else:
		policultura.cria_modo_policultura(Items.Wood, Entities.Tree)(objetivo)

def _cultivo_carrot(objetivo):
	campo.ara()
	policultura.cria_modo_policultura(Items.Carrot, Entities.Carrot)(objetivo)

def inicializa():
	global _ordem
	global _recursos

	dimensao = min(megafazenda.linhas, megafazenda.colunas)
	if dimensao <= 0:
		dimensao = 1

	_ordem = [Items.Power, Items.Bone, Items.Gold, Items.Weird_Substance, Items.Cactus, Items.Pumpkin, Items.Carrot, Items.Wood, Items.Hay]
	_recursos = {
		Items.Hay: {
			"cultivo": policultura.cria_modo_policultura(Items.Hay, Entities.Grass),
			"producao_ciclo": producao_segura((nivel(Unlocks.Polyculture) + 1) * ((nivel(Unlocks.Grass) * campo.n * campo.n) // 2))
		},
		Items.Wood: {
			"cultivo": _cultivo_wood,
			"producao_ciclo": producao_segura((nivel(Unlocks.Polyculture) + 1) * ((nivel(Unlocks.Trees) * 3 * campo.n * campo.n) // 2))
		},
		Items.Carrot: {
			"cultivo": _cultivo_carrot,
			"producao_ciclo": producao_segura((nivel(Unlocks.Polyculture) + 1) * ((nivel(Unlocks.Carrots) * campo.n * campo.n) // 2))
		},
		Items.Pumpkin: {
			"cultivo": abobora.modo_abobora,
			"producao_ciclo": producao_segura(nivel(Unlocks.Pumpkins) * campo.n * campo.n * min(campo.n, 6))
		},
		Items.Power: {
			"cultivo": girassol.modo_girassol,
			"producao_ciclo": producao_segura((nivel(Unlocks.Sunflowers) * 5 * ((campo.n * campo.n) - 9) + 9) - (campo.n * campo.n))
		},
		Items.Cactus: {
			"cultivo": cacto.modo_cacto,
			"producao_ciclo": producao_segura(nivel(Unlocks.Cactus) * (campo.n * campo.n)**2)
		},
		Items.Weird_Substance: {
			"cultivo": policultura.cria_modo_policultura(Items.Weird_Substance, Entities.Tree),
			"producao_ciclo": producao_segura((nivel(Unlocks.Polyculture) + 1) * ((nivel(Unlocks.Trees) * 3 * campo.n * campo.n) // 2))
		},
		Items.Gold: {
			"cultivo": labirinto.modo_labirinto,
			"producao_ciclo": producao_segura(301 * nivel(Unlocks.Mazes) * megafazenda.n_drones * dimensao * dimensao)
		},
		Items.Bone: {
			"cultivo": dinossauro.modo_dinossauro,
			"producao_ciclo": producao_segura(nivel(Unlocks.Dinosaurs) * (campo.n * campo.n)**2)
		}
	}

def precisa(recurso, objetivo):
	return num_items(recurso) < objetivo

def farma_recurso(recurso, objetivo):
	global _recursos
	if not precisa(recurso, objetivo):
		print("    [skip] " + str(recurso) + " ja tem " + str(num_items(recurso)) + "/" + str(objetivo))
		return
	if not pode_produzir(recurso):
		print("    [skip] " + str(recurso) + " nao pode produzir ainda")
		return
	print("    [farma] " + str(recurso) + " de " + str(num_items(recurso)) + " ate " + str(objetivo))
	dados = _recursos[recurso]
	dados["cultivo"](objetivo)
	print("    [ok] " + str(recurso) + " = " + str(num_items(recurso)))

def farma_custo(custo):
	global _ordem
	for recurso in _ordem:
		if recurso not in custo:
			continue
		farma_recurso(recurso, custo[recurso])
