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
chapeus.usa()

ordem = [
	# fase inicial: velocidade e expansao basica
	Unlocks.Speed,
	Unlocks.Plant,
	Unlocks.Grass,          # multiplicador de hay desde cedo
	Unlocks.Expand,
	Unlocks.Expand,
	Unlocks.Speed,
	Unlocks.Grass,          # nivel 2 de grass
	Unlocks.Trees,
	Unlocks.Trees,          # multiplicador de wood/weird
	Unlocks.Carrots,
	Unlocks.Carrots,        # multiplicador de cenoura
	Unlocks.Expand,
	Unlocks.Speed,
	Unlocks.Expand,
	Unlocks.Watering,
	Unlocks.Watering,
	Unlocks.Watering,       # nivel 3 de watering
	Unlocks.Grass,          # nivel 3 de grass
	Unlocks.Carrots,        # nivel 3 de cenoura
	Unlocks.Sunflowers,
	Unlocks.Fertilizer,
	Unlocks.Fertilizer,     # nivel 2 de fertilizer
	Unlocks.Watering,       # nivel 4 de watering
	Unlocks.Speed,
	Unlocks.Pumpkins,
	Unlocks.Watering,       # nivel 5
	Unlocks.Polyculture,
	Unlocks.Speed,
	Unlocks.Expand,
	Unlocks.Fertilizer,     # nivel 3
	Unlocks.Trees,          # nivel 3 de trees
	Unlocks.Grass,          # nivel 4
	Unlocks.Mazes,
	Unlocks.Megafarm,
	Unlocks.Trees,          # nivel 4
	Unlocks.Trees,          # nivel 5
	Unlocks.Carrots,        # nivel 4
	Unlocks.Watering,       # nivel 6
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
	Unlocks.Grass,          # nivel 5
	Unlocks.Trees,          # nivel 6
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
