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

	print("    [mega] n=" + str(tam) + " max_drones=" + str(n_drones) + " faixa=" + str(linhas))

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

def _faz_tarefa_16(acao, nd):
	def t():
		executa_faixa(16, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_17(acao, nd):
	def t():
		executa_faixa(17, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_18(acao, nd):
	def t():
		executa_faixa(18, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_19(acao, nd):
	def t():
		executa_faixa(19, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_20(acao, nd):
	def t():
		executa_faixa(20, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_21(acao, nd):
	def t():
		executa_faixa(21, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_22(acao, nd):
	def t():
		executa_faixa(22, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_23(acao, nd):
	def t():
		executa_faixa(23, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_24(acao, nd):
	def t():
		executa_faixa(24, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_25(acao, nd):
	def t():
		executa_faixa(25, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_26(acao, nd):
	def t():
		executa_faixa(26, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_27(acao, nd):
	def t():
		executa_faixa(27, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_28(acao, nd):
	def t():
		executa_faixa(28, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_29(acao, nd):
	def t():
		executa_faixa(29, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_30(acao, nd):
	def t():
		executa_faixa(30, nd, acao)
	return chapeus.usa_e_faz(t)

def _faz_tarefa_31(acao, nd):
	def t():
		executa_faixa(31, nd, acao)
	return chapeus.usa_e_faz(t)

_fabricas = [
	_faz_tarefa_0,  _faz_tarefa_1,  _faz_tarefa_2,  _faz_tarefa_3,
	_faz_tarefa_4,  _faz_tarefa_5,  _faz_tarefa_6,  _faz_tarefa_7,
	_faz_tarefa_8,  _faz_tarefa_9,  _faz_tarefa_10, _faz_tarefa_11,
	_faz_tarefa_12, _faz_tarefa_13, _faz_tarefa_14, _faz_tarefa_15,
	_faz_tarefa_16, _faz_tarefa_17, _faz_tarefa_18, _faz_tarefa_19,
	_faz_tarefa_20, _faz_tarefa_21, _faz_tarefa_22, _faz_tarefa_23,
	_faz_tarefa_24, _faz_tarefa_25, _faz_tarefa_26, _faz_tarefa_27,
	_faz_tarefa_28, _faz_tarefa_29, _faz_tarefa_30, _faz_tarefa_31
]

def paraleliza_blocos(acao):
	tam = get_world_size()
	nd = max_drones()
	if nd < 1:
		nd = 1
	total = tam * tam
	faixa = util.teto_div(total, nd)

	drones_spawnados = 0
	drones_local = 0
	drones_lista = []

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
			drones_lista.append(drone)
			drones_spawnados += 1
		else:
			tarefa()
			drones_local += 1
		i += 1

	print("    [mega] spawn=" + str(drones_spawnados) + " local=" + str(drones_local) + " total=" + str(drones_spawnados + drones_local))

	for drone in drones_lista:
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
