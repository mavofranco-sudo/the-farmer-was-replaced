_chapeu_padrao = None

def inicializa():
	global _chapeu_padrao
	# descobre qual chapeu esta equipado agora e salva como padrao
	_chapeu_padrao = get_hat()

def usa():
	# reequipa o chapeu padrao (sai do chapeu de dino, colhendo a cauda)
	if _chapeu_padrao != None:
		change_hat(_chapeu_padrao)

def usa_e_faz(acao):
	def funcao():
		return acao()

	return funcao
