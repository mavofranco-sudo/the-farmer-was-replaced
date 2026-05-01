import campo
import chapeus
import dinossauro
import gerenciador
import megafazenda

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
