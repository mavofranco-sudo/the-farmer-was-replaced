import campo
import chapeus
import gerenciador

def _pode_mover(direcao):
	return can_move(direcao)

def _campo_cheio():
	# se nao consegue mover em nenhuma direcao, cobra tomou tudo
	for direcao in campo.direcoes:
		if can_move(direcao):
			return False
	return True

def _serpentina():
	# percorre o campo em serpentina (linha por linha, alternando direcao)
	# garante cobertura total - padrao otimo para cobra
	direcao_h = East
	for lin in range(campo.n):
		# anda horizontalmente pela linha
		for _ in range(campo.n - 1):
			if not move(direcao_h):
				return  # bloqueado pela cauda = campo cheio
		# sobe para proxima linha (se nao for a ultima)
		if lin < campo.n - 1:
			if not move(North):
				return
			direcao_h = West if direcao_h == East else East

def _ciclo_dino():
	campo.vai_para(0, 0)
	change_hat(Hats.Dinosaur_Hat)
	_serpentina()
	# troca o chapeu para colher os ossos (cauda vira ossos ao desequipar)
	chapeus.usa()

def modo_dinossauro(objetivo):
	while gerenciador.precisa(Items.Bone, objetivo):
		_ciclo_dino()
