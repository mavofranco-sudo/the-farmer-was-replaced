_n_chapeus = 0
_chapeus = []

def inicializa():
	global _n_chapeus
	global _chapeus

	_chapeus = []
	for chapeu in Hats:
		if chapeu == Hats.Dinosaur_Hat:
			continue
		if num_unlocked(chapeu):
			_chapeus.append(chapeu)

	_n_chapeus = len(_chapeus)

def tem_chapeu():
	return _n_chapeus > 0

def usa():
	if not tem_chapeu():
		return
	indice = _n_chapeus * random() // 1
	change_hat(_chapeus[indice])

def usa_e_faz(acao):
	def funcao():
		usa()
		return acao()

	return funcao
