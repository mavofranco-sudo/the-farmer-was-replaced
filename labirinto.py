import campo
import megafazenda

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
	# custo baseado no tamanho do campo, nao das faixas
	tam = get_world_size()
	return _nivel_mazes() * tam

def _ciclo_labirinto(objetivo):
	tam = get_world_size()
	# labirinto sempre abre no centro do campo
	x_meio = tam // 2
	y_meio = tam // 2
	custo = _custo_entrada()

	campo.vai_para(x_meio, y_meio)
	campo.cultiva(Entities.Bush)

	for _ in range(301):
		if num_items(Items.Gold) >= objetivo:
			break
		if num_items(Items.Weird_Substance) < custo:
			break
		use_item(Items.Weird_Substance, custo)

		resultado = measure()
		if resultado == None:
			continue

		x = get_pos_x()
		y = get_pos_y()
		_navega_para_tesouro(x, y)

	if get_entity_type() == Entities.Treasure:
		harvest()
	elif get_entity_type() != None and can_harvest():
		harvest()

def _garante_weird_substance(objetivo):
	custo = _custo_entrada()
	# margem para varios ciclos de 301 uses
	necessario = custo * 301 * 4
	if num_items(Items.Weird_Substance) < necessario:
		print("    [labirinto] abastecer Weird_Substance: " + str(necessario))
		import policultura
		policultura.cria_modo_policultura(Items.Weird_Substance, Entities.Tree)(necessario)

def modo_labirinto(objetivo):
	while num_items(Items.Gold) < objetivo:
		_garante_weird_substance(objetivo)
		print("    [labirinto] gold=" + str(num_items(Items.Gold)) + "/" + str(objetivo) +
			" ws=" + str(num_items(Items.Weird_Substance)) +
			" custo=" + str(_custo_entrada()))
		_ciclo_labirinto(objetivo)
	clear()
	campo.ara()
