_requisitos = {
	Hats.Dinosaur_Hat: Unlocks.Dinosaurs,
}

def chapeu_disponivel(chapeu):
	if chapeu in _requisitos:
		return num_unlocked(_requisitos[chapeu]) > 0
	return num_unlocked(chapeu) > 0

def lista_chapeus_disponiveis():
	disponiveis = []
	for chapeu in Hats:
		if chapeu_disponivel(chapeu):
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
