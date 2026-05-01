_n_chapeus = 0
_chapeus = []

_chapeus_bloqueados = [Hats.Dinosaur_Hat]

def inicializa():
	global _n_chapeus
	global _chapeus

	_chapeus = []
	for chapeu in Hats:
		if chapeu in _chapeus_bloqueados:
			continue
		if num_unlocked(chapeu):
			_chapeus.append(chapeu)

	_n_chapeus = len(_chapeus)

def tem_chapeu():
	return _n_chapeus > 0

def usa():
	if not tem_chapeu():
		return
	indice = (_n_chapeus - 1) * random() // 1
	if indice >= _n_chapeus:
		indice = _n_chapeus - 1
	change_hat(_chapeus[indice])

def usa_e_faz(acao):
	def funcao():
		usa()
		return acao()

	return funcao
