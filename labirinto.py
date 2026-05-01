import campo
import megafazenda

_x_tesouro = 0
_y_tesouro = 0

def _navega_para_tesouro(x_ini, y_ini):
	visitados = []
	visitados.append([x_ini, y_ini])

	# pilha: [x, y, indice_direcao, direcao_volta]
	pilha = [[x_ini, y_ini, 0, None]]

	while len(pilha) > 0:
		topo = pilha[len(pilha) - 1]
		x = topo[0]
		y = topo[1]
		idx = topo[2]
		volta = topo[3]

		if get_entity_type() == Entities.Treasure:
			return True

		if idx >= len(campo.direcoes):
			pilha.pop()
			if volta != None:
				move(volta)
			continue

		topo[2] = idx + 1
		direcao = campo.direcoes[idx]
		proximo = campo.proximo(x, y, direcao)
		x_p = proximo[0]
		y_p = proximo[1]

		ja_visitado = False
		for v in visitados:
			if v[0] == x_p and v[1] == y_p:
				ja_visitado = True
				break

		if ja_visitado:
			continue
		if not can_move(direcao):
			continue

		visitados.append([x_p, y_p])
		move(direcao)
		pilha.append([x_p, y_p, 0, campo.opostos[direcao]])

	return False

def _nivel_mazes():
	n = num_unlocked(Unlocks.Mazes)
	if n == 0:
		return 1
	return 2 ** (n - 1)

def _custo_entrada():
	dimensao = min(megafazenda.linhas, megafazenda.colunas)
	if dimensao < 1:
		dimensao = 1
	return _nivel_mazes() * dimensao

def tarefa(objetivo):
	def funcao():
		custo = _custo_entrada()
		x_meio = get_pos_x() + megafazenda.colunas // 2
		y_meio = get_pos_y() + megafazenda.linhas // 2

		while num_items(Items.Gold) < objetivo:
			campo.vai_para(x_meio, y_meio)
			campo.cultiva(Entities.Bush)

			for _ in range(301):
				if num_items(Items.Weird_Substance) < custo:
					break
				use_item(Items.Weird_Substance, custo)

				resultado = measure()
				if resultado == None:
					continue

				x = get_pos_x()
				y = get_pos_y()
				_navega_para_tesouro(x, y)

			harvest()

	return funcao

def _garante_weird_substance(objetivo):
	# calcula quantas WS sao necessarias para todos os drones completarem
	custo = _custo_entrada()
	n_drones = megafazenda.n_drones
	if n_drones < 1:
		n_drones = 1
	# cada drone faz ate 301 uses por ciclo, estimar margem generosa
	necessario = custo * 301 * n_drones * 2
	if num_items(Items.Weird_Substance) < necessario:
		print("    [labirinto] abastecer Weird_Substance: " + str(necessario))
		import policultura
		policultura.cria_modo_policultura(Items.Weird_Substance, Entities.Tree)(necessario)

def modo_labirinto(objetivo):
	while num_items(Items.Gold) < objetivo:
		_garante_weird_substance(objetivo)
		megafazenda.paraleliza_blocos(tarefa(objetivo))
	clear()
	campo.ara()
