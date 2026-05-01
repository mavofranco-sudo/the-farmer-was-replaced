import campo
import chapeus
import util

n_drones = 0
linhas = 1
colunas = 1

def inicializa():
	global n_drones
	global linhas
	global colunas

	n_drones = max_drones()
	tam = get_world_size()

	if n_drones > 0:
		linhas = util.teto_div(tam * tam, n_drones)
	else:
		linhas = tam * tam
	colunas = 1

	print("    [mega] n=" + str(tam) + " drones=" + str(n_drones) + " faixa=" + str(linhas))

def executa_faixa(indice, nd, acao):
	tam = get_world_size()
	total = tam * tam
	faixa = util.teto_div(total, nd)
	inicio = indice * faixa
	fim = inicio + faixa
	if fim > total:
		fim = total
	j = inicio
	while j < fim:
		cx = j // tam
		cy = j % tam
		campo.vai_para(cx, cy)
		acao()
		j += 1

def _faz_tarefa_0(acao, nd):
	def t():
		executa_faixa(0, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_1(acao, nd):
	def t():
		executa_faixa(1, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_2(acao, nd):
	def t():
		executa_faixa(2, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_3(acao, nd):
	def t():
		executa_faixa(3, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_4(acao, nd):
	def t():
		executa_faixa(4, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_5(acao, nd):
	def t():
		executa_faixa(5, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_6(acao, nd):
	def t():
		executa_faixa(6, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_7(acao, nd):
	def t():
		executa_faixa(7, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_8(acao, nd):
	def t():
		executa_faixa(8, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_9(acao, nd):
	def t():
		executa_faixa(9, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_10(acao, nd):
	def t():
		executa_faixa(10, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_11(acao, nd):
	def t():
		executa_faixa(11, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_12(acao, nd):
	def t():
		executa_faixa(12, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_13(acao, nd):
	def t():
		executa_faixa(13, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_14(acao, nd):
	def t():
		executa_faixa(14, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_15(acao, nd):
	def t():
		executa_faixa(15, nd, acao)
	return chapeus.usa_e_faz(t)

_fabricas = [
	_faz_tarefa_0, _faz_tarefa_1, _faz_tarefa_2, _faz_tarefa_3,
	_faz_tarefa_4, _faz_tarefa_5, _faz_tarefa_6, _faz_tarefa_7,
	_faz_tarefa_8, _faz_tarefa_9, _faz_tarefa_10, _faz_tarefa_11,
	_faz_tarefa_12, _faz_tarefa_13, _faz_tarefa_14, _faz_tarefa_15
]

def paraleliza_blocos(acao):
	tam = get_world_size()
	nd = max_drones()
	if nd < 1:
		nd = 1
	total = tam * tam
	faixa = util.teto_div(total, nd)
	drones = []

	i = 0
	while i < nd and i < len(_fabricas):
		inicio = i * faixa
		if inicio >= total:
			break
		cx = inicio // tam
		cy = inicio % tam
		campo.vai_para(cx, cy)
		tarefa = _fabricas[i](acao, nd)
		drone = spawn_drone(tarefa)
		if drone:
			drones.append(drone)
		else:
			tarefa()
		i += 1

	for drone in drones:
		wait_for(drone)

def paraleliza_linha(acao, por_linha=True):
	tam = get_world_size()
	drones = []
	for i in range(tam):
		if por_linha:
			campo.vai_para(0, i)
		else:
			campo.vai_para(i, 0)
		drone = spawn_drone(chapeus.usa_e_faz(acao))
		if drone:
			drones.append(drone)
		else:
			chapeus.usa_e_faz(acao)()
	for drone in drones:
		wait_for(drone)
