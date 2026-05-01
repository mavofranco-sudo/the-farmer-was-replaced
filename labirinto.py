import campo
import gerenciador
import megafazenda

_x_tesouro = 0
_y_tesouro = 0

def _navega_para_tesouro(x_ini, y_ini):
	global _x_tesouro
	global _y_tesouro

	visitados = set()
	visitados.add((x_ini, y_ini))

	# pilha: [x, y, indice_direcao, caminho_de_volta]
	pilha = [[x_ini, y_ini, 0, []]]

	while len(pilha) > 0:
		topo = pilha[len(pilha) - 1]
		x = topo[0]
		y = topo[1]
		idx = topo[2]
		caminho = topo[3]

		if get_entity_type() == Entities.Treasure:
			return True

		if idx >= len(campo.direcoes):
			# backtrack
			pilha.pop()
			if len(caminho) > 0:
				move(caminho[len(caminho) - 1])
			continue

		topo[2] = idx + 1

		direcao = campo.direcoes[idx]
		proximo = campo.proximo(x, y, direcao)
		x_p = proximo[0]
		y_p = proximo[1]

		if not can_move(direcao):
			continue
		if (x_p, y_p) in visitados:
			continue

		visitados.add((x_p, y_p))
		move(direcao)
		pilha.append([x_p, y_p, 0, [campo.opostos[direcao]]])

	return False

def tarefa(objetivo):
	def funcao():
		global _x_tesouro
		global _y_tesouro

		custo = gerenciador.nivel(Unlocks.Mazes) * min(megafazenda.linhas, megafazenda.colunas)
		x_meio = get_pos_x() + megafazenda.colunas // 2
		y_meio = get_pos_y() + megafazenda.linhas // 2

		while gerenciador.precisa(Items.Gold, objetivo):
			campo.vai_para(x_meio, y_meio)
			campo.cultiva(Entities.Bush)

			for _ in range(301):
				if num_items(Items.Weird_Substance) < custo:
					gerenciador.farma_recurso(Items.Weird_Substance, custo * 10)

				if num_items(Items.Weird_Substance) >= custo:
					use_item(Items.Weird_Substance, custo)

				resultado = measure()
				if resultado == None:
					continue

				x = get_pos_x()
				y = get_pos_y()
				_x_tesouro = resultado[0]
				_y_tesouro = resultado[1]
				_navega_para_tesouro(x, y)
			harvest()

	return funcao

def modo_labirinto(objetivo):
	megafazenda.paraleliza_blocos(tarefa(objetivo))
	clear()
	campo.ara()
