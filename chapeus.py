def inicializa():
	pass

def usa():
	if num_unlocked(Unlocks.Dinosaurs) > 0:
		change_hat(Hats.Straw_Hat)

def usa_e_faz(acao):
	def funcao():
		return acao()

	return funcao
