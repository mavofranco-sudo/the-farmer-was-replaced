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

# 1. Velocidade (20 grama) — primeiro pra farmar mais rapido
desbloqueia(Unlocks.Speed)

# 2. Grama (200 grama) — aumenta producao de hay
desbloqueia(Unlocks.Grass)

# A partir daqui continua pelos demais unlocks em ordem util
conquistas = list(Unlocks)
for conquista in conquistas:
	if get_cost(conquista):
		desbloqueia(conquista)
