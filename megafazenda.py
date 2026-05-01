import campo
import chapeus
import util

n_drones = 0
linhas = 0
colunas = 0

def inicializa():
	global n_drones
	global linhas
	global colunas

	# sempre usa get_world_size() direto
	tam = get_world_size()
	n_drones = max_drones()

	drones_por_linha = util.sqrt_2(n_drones)
	if drones_por_linha < 1:
		drones_por_linha = 1

	drones_por_coluna = n_drones // drones_por_linha
	if drones_por_coluna < 1:
		drones_por_coluna = 1

	linhas = util.teto_div(tam, drones_por_linha)
	if linhas < 1:
		linhas = 1

	colunas = util.teto_div(tam, drones_por_coluna)
	if colunas % 2 == 1:
		colunas += 1
	if colunas < 1:
		colunas = 1

	print("    [mega] n=" + str(tam) + " drones=" + str(n_drones) +
		" bloco=" + str(colunas) + "x" + str(linhas))

def paraleliza_linha(acao, por_linha=True):
	drones = []
	resultados = []
	tam = get_world_size()

	for i in range(tam):
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

	# usa get_world_size() direto - nunca campo.n que pode estar desatualizado
	tam = get_world_size()
	lin = linhas
	col = colunas
	if lin < 1:
		lin = 1
	if col < 1:
		col = 1

	x = 0
	while x < tam:
		y = 0
		while y < tam:
			campo.vai_para(x, y)
			drone = spawn_drone(chapeus.usa_e_faz(acao))
			if drone:
				drones.append(drone)
			else:
				resultados.append(chapeus.usa_e_faz(acao)())
			y += lin
		x += col

	for drone in drones:
		resultados.append(wait_for(drone))

	return resultados
