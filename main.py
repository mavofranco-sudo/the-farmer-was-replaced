import campo
import chapeus
import gerenciador
import megafazenda

def inicializa(conquista=None):
	campo.inicializa()
	chapeus.inicializa()
	megafazenda.inicializa()
	gerenciador.inicializa()

	if conquista == Unlocks.Expand:
		campo.ara()

def desbloqueia(conquista):
	if get_cost(conquista):
		print(conquista)
		gerenciador.farma_custo(get_cost(conquista))
		unlock(conquista)
		do_a_flip()
		inicializa(conquista)

clear()
inicializa()
chapeus.usa()

ordem = [
	Unlocks.Speed,
	Unlocks.Plant,
	Unlocks.Expand,
	Unlocks.Expand,
	Unlocks.Speed,
	Unlocks.Carrots,
	Unlocks.Grass,
	Unlocks.Trees,
	Unlocks.Trees,
	Unlocks.Expand,
	Unlocks.Carrots,
	Unlocks.Speed,
	Unlocks.Expand,
	Unlocks.Watering,
	Unlocks.Watering,
	Unlocks.Carrots,
	Unlocks.Grass,
	Unlocks.Sunflowers,
	Unlocks.Fertilizer,
	Unlocks.Watering,
	Unlocks.Speed,
	Unlocks.Pumpkins,
	Unlocks.Watering,
	Unlocks.Polyculture,
	Unlocks.Speed,
	Unlocks.Expand,
	Unlocks.Fertilizer,
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
