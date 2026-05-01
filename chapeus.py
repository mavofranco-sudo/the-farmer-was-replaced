def inicializa():
	pass

def usa():
	if num_unlocked(Unlocks.Dinosaurs) > 0:
		chapeu = getattr(Hats, "Straw_Hat")
		change_hat(chapeu)

def usa_e_faz(acao):
	def funcao():
		return acao()

	return funcao
