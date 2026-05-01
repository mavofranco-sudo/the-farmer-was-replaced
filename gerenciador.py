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

def calcula_energia_rec(recurso, objetivo):
	global _recursos

	resposta = 0

	if precisa(recurso, objetivo):
		if not pode_produzir(recurso):
			return 0
		dados = _recursos[recurso]

		objetivo_real = (objetivo - num_items(recurso))
		n_ciclos = util.teto_div(objetivo_real, dados["producao_ciclo"])
		if dados["ciclo_inicio"]:
			n_ciclos += 1
		custo_real = dados["custo_ciclo"] * n_ciclos
		custo_energia_real = dados["custo_energia_ciclo"] * n_ciclos

		resposta = custo_energia_real

		custo = get_cost(dados["planta"])
		for item in custo:
			qtd = custo[item]
			resposta += calcula_energia_rec(item, qtd * custo_real)

	return resposta

def calcula_energia(objetivos):
	global _ordem

	resposta = 0

	for recurso in _ordem:
		if recurso not in objetivos:
			continue
		resposta += calcula_energia_rec(recurso, objetivos[recurso])

	return util.teto_div(resposta, 30)

def precisa(recurso, objetivo):
	return num_items(recurso) < objetivo

def alcanca_objetivos_rec(recurso, objetivo):
	global _recursos

	if precisa(recurso, objetivo):
		if not pode_produzir(recurso):
			return
		dados = _recursos[recurso]

		objetivo_real = (objetivo - num_items(recurso))
		n_ciclos = util.teto_div(objetivo_real, dados["producao_ciclo"])
		if dados["ciclo_inicio"]:
			n_ciclos += 1
		custo_real = dados["custo_ciclo"] * n_ciclos

		custo = get_cost(dados["planta"])
		for item in custo:
			qtd = custo[item]
			alcanca_objetivos_rec(item, qtd * custo_real)

		dados["cultivo"](objetivo)

def alcanca_objetivos(objetivos):
	global _ordem

	energia = calcula_energia(objetivos)
	if energia > 0 and pode_produzir(Items.Power):
		objetivos[Items.Power] = energia

	for recurso in _ordem:
		if recurso not in objetivos:
			continue
		alcanca_objetivos_rec(recurso, objetivos[recurso])

def conquista_alcancavel(conquista):
	if completada(conquista):
		return False
	custo = get_cost(conquista)
	for recurso in custo:
		if not pode_produzir(recurso):
			return False
	return True

def escolha_conquista(conquistas):
	melhor_conquista = None
	menor_custo = -1

	for conquista in conquistas:
		if not conquista_alcancavel(conquista):
			continue
		custo = calcula_energia(get_cost(conquista))
		if melhor_conquista is None or custo < menor_custo:
			menor_custo = custo
			melhor_conquista = conquista

	return melhor_conquista

