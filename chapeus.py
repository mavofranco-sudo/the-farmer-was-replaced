def inicializa():
	pass

def usa():
	change_hat(Hats.Farmer_Hat)

def usa_e_faz(acao):
	def funcao():
		return acao()

	return funcao
