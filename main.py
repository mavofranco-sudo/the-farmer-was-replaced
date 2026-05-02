import campo
import chapeus
import dinossauro
import gerenciador
import megafazenda
import abobora
import girassol
import girassol_v2
import policultura

def inicializa(conquista=None):
	campo.inicializa()
	chapeus.inicializa()
	megafazenda.inicializa()
	gerenciador.inicializa()

	if conquista == Unlocks.Expand:
		campo.ara()

	if num_unlocked(Unlocks.Dinosaurs) > 0:
		dinossauro.configura_hats(Hats.Dinosaur_Hat, Hats.Straw_Hat)

def desbloqueia(conquista):
	custo = get_cost(conquista)
	if custo:
		print(">>> inicio: " + str(conquista))
		print("    custo: " + str(custo))
		gerenciador.farma_custo(custo)
		print("    farmado, desbloqueando...")
		unlock(conquista)
		do_a_flip()
		inicializa(conquista)
		print("<<< concluido: " + str(conquista))

def _noop():
	pass

def _prepara_cenouras_para_abobora():
	# garante cenouras suficientes para um ciclo completo de aboboras
	n = get_world_size()
	minimo = 512 * n * n + n * n * 2 + 100
	if num_items(Items.Carrot) >= minimo:
		return
	policultura.cria_modo_policultura_com_reabastecimento(
		Items.Carrot, Entities.Carrot,
		_noop
	)(minimo)

def _power_minimo_farm():
	# power suficiente para 1 ciclo de aboboras: n² acoes * margem
	n = get_world_size()
	return n * n * 5 + 200

def _prepara_power_farm():
	# reabastece so o necessario para 1 ciclo - evita ficar farmando power em excesso
	if not gerenciador.pode_produzir(Items.Power):
		return
	minimo = _power_minimo_farm()
	if num_items(Items.Power) >= minimo:
		return
	if not girassol_v2.tem_cenouras_suficientes():
		_prepara_cenouras_para_abobora()
	if girassol_v2.tem_cenouras_suficientes():
		print("  [farm] reabastecendo power ate " + str(minimo))
		girassol_v2.modo_girassol(minimo)

def farm_aboboras_infinito(objetivo):
	print(">>> MODO FARM: " + str(objetivo) + " aboboras")
	ciclo = 0
	while num_items(Items.Pumpkin) < objetivo:
		ciclo += 1
		_prepara_cenouras_para_abobora()
		_prepara_power_farm()
		if ciclo % 100 == 1:
			print("  [farm] ciclo=" + str(ciclo) +
				" abob=" + str(num_items(Items.Pumpkin)) + "/" + str(objetivo) +
				" power=" + str(num_items(Items.Power)))
		abobora.modo_abobora(num_items(Items.Pumpkin) + get_world_size() * get_world_size())
	print(">>> OBJETIVO ATINGIDO: " + str(num_items(Items.Pumpkin)) + " aboboras")

clear()
inicializa()

ordem = [
	# fase 1: base
	Unlocks.Speed,
	Unlocks.Plant,
	Unlocks.Grass,
	Unlocks.Expand,
	Unlocks.Expand,
	Unlocks.Speed,
	Unlocks.Grass,
	Unlocks.Carrots,
	Unlocks.Trees,
	Unlocks.Trees,
	Unlocks.Carrots,
	Unlocks.Expand,
	Unlocks.Speed,
	Unlocks.Expand,
	Unlocks.Watering,
	Unlocks.Watering,
	Unlocks.Watering,
	Unlocks.Grass,
	Unlocks.Carrots,
	Unlocks.Sunflowers,
	Unlocks.Fertilizer,
	Unlocks.Fertilizer,
	Unlocks.Watering,
	Unlocks.Speed,
	Unlocks.Pumpkins,
	Unlocks.Watering,
	Unlocks.Polyculture,
	Unlocks.Speed,
	Unlocks.Expand,
	Unlocks.Fertilizer,
	Unlocks.Trees,
	Unlocks.Grass,
	Unlocks.Mazes,
	Unlocks.Megafarm,
	Unlocks.Trees,
	Unlocks.Trees,
	Unlocks.Carrots,
	Unlocks.Watering,
	Unlocks.Pumpkins,
	Unlocks.Pumpkins,
	Unlocks.Expand,
	Unlocks.Cactus,
	Unlocks.Dinosaurs,
	Unlocks.Dinosaurs,
	Unlocks.Polyculture,
	Unlocks.Mazes,
	Unlocks.Mazes,
	Unlocks.Megafarm,
	Unlocks.Megafarm,
	Unlocks.Grass,
	Unlocks.Trees,
	Unlocks.Fertilizer,
	Unlocks.Fertilizer,
	Unlocks.Watering,
	Unlocks.Carrots,
	Unlocks.Carrots,
	Unlocks.Pumpkins,
	Unlocks.Pumpkins,
	Unlocks.Expand,
	Unlocks.Megafarm,
	Unlocks.Cactus,
	Unlocks.Cactus,
	Unlocks.Dinosaurs,
	Unlocks.Dinosaurs,
	Unlocks.Dinosaurs,
	Unlocks.Mazes,
	Unlocks.Leaderboard,
]

for conquista in ordem:
	desbloqueia(conquista)

# fase final: farm de 100 milhoes de aboboras
farm_aboboras_infinito(100000000)
