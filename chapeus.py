_chapeus_bloqueados = [Hats.Dinosaur_Hat]

def lista_chapeus_disponiveis():
	disponiveis = []
	for chapeu in Hats:
		if chapeu in _chapeus_bloqueados:
			continue
		if num_unlocked(chapeu):
			disponiveis.append(chapeu)
	return disponiveis

def usa():
	disponiveis = lista_chapeus_disponiveis()
	if not disponiveis:
		return
	n = len(disponiveis)
	indice = (n - 1) * random() // 1
	if indice >= n:
		indice = n - 1
	change_hat(disponiveis[indice])

def inicializa():
	pass

def usa_e_faz(acao):
	def funcao():
		usa()
		return acao()

	return funcao
