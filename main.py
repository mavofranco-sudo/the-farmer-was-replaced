import campo
import chapeus
import dinossauro
import gerenciador
import megafazenda
import abobora
import girassol
import girassol_v2
import policultura
import cacto

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

def farm_power_infinito():
	print(">>> MODO FARM POWER: objetivo 12000/min")
	if not girassol_v2.tem_cenouras_suficientes():
		n = get_world_size()
		minimo_cenoura = n * n * 3
		print("  [power] preparando cenouras: " + str(minimo_cenoura))
		policultura.cria_modo_policultura_com_reabastecimento(
			Items.Carrot, Entities.Carrot, _noop
		)(minimo_cenoura)

	ciclo = 0
	t_inicio = get_time()
	power_inicio = num_items(Items.Power)

	while True:
		ciclo += 1
		if not girassol_v2.tem_cenouras_suficientes():
			n = get_world_size()
			minimo_cenoura = n * n * 3
			policultura.cria_modo_policultura_com_reabastecimento(
				Items.Carrot, Entities.Carrot, _noop
			)(minimo_cenoura)

		power_antes = num_items(Items.Power)
		girassol_v2.modo_girassol(power_antes + get_world_size() * get_world_size())
		power_depois = num_items(Items.Power)

		t_agora = get_time()
		dur_total = t_agora - t_inicio
		power_total = power_depois - power_inicio
		ritmo = 0
		if dur_total > 0:
			ritmo = (power_total * 60) // dur_total

		print("  [power] ciclo=" + str(ciclo) +
			" power=" + str(power_depois) +
			" gerado=" + str(power_depois - power_antes) +
			" ritmo=" + str(ritmo) + "/min")

		if ritmo >= 12000:
			print(">>> OBJETIVO ATINGIDO: " + str(ritmo) + "/min (meta: 12000/min)")
			return

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

# farm de power apos aboboras
farm_power_infinito()

# farm de cactus: 3 ciclos completos

def _farm_cactus_ciclos(num_ciclos):
	ciclo = 0
	while ciclo < num_ciclos:
		ciclo += 1
		n = get_world_size()
		print(">>> CICLO CACTUS " + str(ciclo) + "/" + str(num_ciclos))

		# garante aboboras para 1 campo cheio
		aboboras_necessarias = n * n * 64
		if num_items(Items.Pumpkin) < aboboras_necessarias:
			print("  [cactus] farmando aboboras: " + str(aboboras_necessarias))
			farm_aboboras_infinito(aboboras_necessarias)

		# garante power antes de comecar
		if girassol_v2.tem_cenouras_suficientes():
			power_min = n * n * 10 + 500
			if num_items(Items.Power) < power_min:
				print("  [cactus] reabastecendo power ate " + str(power_min))
				girassol_v2.modo_girassol(power_min)

		# 1 ciclo completo de cactus
		cacto.modo_cacto(num_items(Items.Cactus) + n * n * n * n)
		print(">>> CACTUS ciclo=" + str(ciclo) + " total=" + str(num_items(Items.Cactus)))

_farm_cactus_ciclos(3)



