import campo
import chapeus
import util

n_drones = 0
linhas = 0
colunas = 0

_limite_linhas = 0
_limite_colunas = 0

def inicializa():
	global n_drones
	global linhas
	global colunas
	global _limite_linhas
	global _limite_colunas

	n_drones = max_drones()

	drones_por_linha = util.sqrt_2(n_drones)
	if drones_por_linha < 1:
		drones_por_linha = 1

	drones_por_coluna = n_drones // drones_por_linha
	if drones_por_coluna < 1:
		drones_por_coluna = 1

	# bloco de cada drone (arredondado para cima para cobrir campo todo)
	linhas = util.teto_div(campo.n, drones_por_linha)
	if linhas < 1:
		linhas = 1

	colunas = util.teto_div(campo.n, drones_por_coluna)
	# colunas deve ser par para movimento_bloco funcionar corretamente
	if colunas % 2 == 1:
		colunas += 1
	if colunas < 1:
		colunas = 1

	# limites: quantas celulas o grid de drones cobre
	# nao pode ultrapassar campo.n
	_limite_linhas = min(linhas * drones_por_linha, campo.n)
	_limite_colunas = min(colunas * drones_por_coluna, campo.n)

	print("    [mega] n=" + str(campo.n) + " drones=" + str(n_drones) +
		" bloco=" + str(colunas) + "x" + str(linhas) +
		" cobertura=" + str(_limite_colunas) + "x" + str(_limite_linhas))

def paraleliza_linha(acao, por_linha=True):
	drones = []
	resultados = []

	for i in range(campo.n):
		if por_linha:
			campo.vai_para(0, i)
		else:
			campo.vai_para(i, 0)

		drone = spawn_drone(chapeus.usa_e_faz(acao))
		if drone:
			drones.append(drone)
		else:
			resultados.append(chapeus.usa_e_faz(acao)())

	for drone in drones:
		resultados.append(wait_for(drone))

	return resultados

def paraleliza_blocos(acao):
	drones = []
	resultados = []

	x = 0
	while x < campo.n:
		y = 0
		while y < campo.n:
			campo.vai_para(x, y)
			drone = spawn_drone(chapeus.usa_e_faz(acao))
			if drone:
				drones.append(drone)
			else:
				resultados.append(chapeus.usa_e_faz(acao)())
			y += linhas
		x += colunas

	for drone in drones:
		resultados.append(wait_for(drone))

	return resultados
