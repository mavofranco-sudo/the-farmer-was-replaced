import campo
import chapeus
import dinossauro
import gerenciador
import megafazenda
import abobora
import girassol_v2
import policultura
import cacto
import labirinto

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
		t0 = get_time()
		print(">>> inicio: " + str(conquista) + " custo=" + str(custo))
		gerenciador.farma_custo(custo)
		unlock(conquista)
		do_a_flip()
		inicializa(conquista)
		dur = (get_time() - t0) * 1000 // 1
		print("<<< concluido: " + str(conquista) + " (" + str(dur) + "ms)")

def _noop():
	pass

def _prepara_cenouras(minimo):
	if num_items(Items.Carrot) >= minimo:
		return
	policultura.cria_modo_policultura_com_reabastecimento(
		Items.Carrot, Entities.Carrot, _noop
	)(minimo)

def _prepara_power(minimo):
	if not gerenciador.pode_produzir(Items.Power):
		return
	if num_items(Items.Power) >= minimo:
		return
	if not girassol_v2.tem_cenouras_suficientes():
		n = get_world_size()
		_prepara_cenouras(n * n * 3)
	if girassol_v2.tem_cenouras_suficientes():
		girassol_v2.modo_girassol(minimo)

def farm_aboboras(objetivo):
	print(">>> FARM ABOBORAS: " + str(objetivo))
	while num_items(Items.Pumpkin) < objetivo:
		n = get_world_size()
		_prepara_cenouras(512 * n * n + n * n * 2 + 100)
		_prepara_power(n * n * 5 + 200)
		abobora.modo_abobora(num_items(Items.Pumpkin) + n * n)
	print(">>> ABOBORAS OK: " + str(num_items(Items.Pumpkin)))

def farm_power_ate(ritmo_objetivo):
	print(">>> FARM POWER: objetivo " + str(ritmo_objetivo) + "/min")
	n = get_world_size()
	if not girassol_v2.tem_cenouras_suficientes():
		_prepara_cenouras(n * n * 3)
	ciclo = 0
	t_inicio = get_time()
	power_inicio = num_items(Items.Power)
	while True:
		ciclo += 1
		if not girassol_v2.tem_cenouras_suficientes():
			_prepara_cenouras(n * n * 3)
		power_antes = num_items(Items.Power)
		girassol_v2.modo_girassol(power_antes + n * n)
		power_depois = num_items(Items.Power)
		t_agora = get_time()
		dur_total = t_agora - t_inicio
		ritmo = 0
		if dur_total > 0:
			ritmo = ((power_depois - power_inicio) * 60) // dur_total
		print("  [power] ciclo=" + str(ciclo) + " power=" + str(power_depois) + " ritmo=" + str(ritmo) + "/min")
		if ritmo >= ritmo_objetivo:
			print(">>> POWER OK: " + str(ritmo) + "/min")
			return

def farm_cactus_ciclos(num_ciclos):
	ciclo = 0
	while ciclo < num_ciclos:
		ciclo += 1
		n = get_world_size()
		print(">>> CICLO CACTUS " + str(ciclo) + "/" + str(num_ciclos))
		aboboras_necessarias = n * n * 64
		if num_items(Items.Pumpkin) < aboboras_necessarias:
			farm_aboboras(aboboras_necessarias)
		power_min = n * n * 10 + 500
		if num_items(Items.Power) < power_min:
			_prepara_power(power_min)
		cacto.modo_cacto(num_items(Items.Cactus) + n * n * n * n)
		print(">>> CACTUS ciclo=" + str(ciclo) + " total=" + str(num_items(Items.Cactus)))

# =========================================
clear()
inicializa()

ordem = [
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

farm_aboboras(100000000)
farm_power_ate(12000)
farm_cactus_ciclos(3)
