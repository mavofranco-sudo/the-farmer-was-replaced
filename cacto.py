def _cria_cacto_faixa(x_ini, x_fim):
	def fn():
		tam = get_world_size()
		x = x_ini
		while True:
			if x >= x_fim:
				x = x_ini
			y = 0
			while y < tam:
				cx = get_pos_x()
				cy = get_pos_y()
				# move para (x, y)
				while cx < x:
					move(East)
					cx += 1
				while cx > x:
					move(West)
					cx -= 1
				while cy < y:
					move(North)
					cy += 1
				while cy > y:
					move(South)
					cy -= 1
				# trata a celula
				if get_ground_type() != Grounds.Soil:
					if can_harvest():
						harvest()
					till()
				else:
					if can_harvest():
						harvest()
				if num_items(Items.Water) > 0:
					use_item(Items.Water)
				if num_items(Items.Fertilizer) > 0:
					use_item(Items.Fertilizer)
				if get_entity_type() != Entities.Cactus:
					plant(Entities.Cactus)
				y += 1
			x += 1
	return fn

def cacto():
	tam = get_world_size()
	nd = max_drones()
	if nd < 1:
		nd = 1
	faixa = tam // nd
	if faixa < 1:
		faixa = 1
	drones = []
	i = 0
	while i < nd:
		x_ini = i * faixa
		if i == nd - 1:
			x_fim = tam
		else:
			x_fim = x_ini + faixa
		d = spawn_drone(_cria_cacto_faixa(x_ini, x_fim))
		if d:
			drones.append(d)
		else:
			_cria_cacto_faixa(x_ini, x_fim)()
		i += 1
	for d in drones:
		wait_for(d)

cacto()
