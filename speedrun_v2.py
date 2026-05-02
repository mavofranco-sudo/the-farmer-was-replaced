ws = get_world_size()
rws = range(ws)
# Maze
leftOf = {North:West, East:North, South:East, West:South}
rightOf = {North:East, East:South, South:West, West:North}
oppositeOf = {North:South, East:West, South:North, West:East}
currentDirection = North
l = -1
substance = -1

def _move_to(x, y):
	cx = get_pos_x()
	cy = get_pos_y()
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

def slowest_automation():
	s = get_time()
	quick_print("Slowest Reset")
	unlock_tech(Unlocks.Speed)
	unlock_tech(Unlocks.Plant)
	unlock_tech(Unlocks.Carrots)
	unlock_tech(Unlocks.Speed)
	unlock_tech(Unlocks.Watering)
	unlock_tech(Unlocks.Trees)
	unlock_tech(Unlocks.Speed)
	unlock_tech(Unlocks.Expand)
	unlock_tech(Unlocks.Expand)
	unlock_tech(Unlocks.Speed)
	unlock_tech(Unlocks.Fertilizer)
	unlock_tech(Unlocks.Pumpkins)
	unlock_tech(Unlocks.Expand)
	unlock_tech(Unlocks.Fertilizer)
	unlock_tech(Unlocks.Fertilizer)
	unlock_tech(Unlocks.Grass)
	unlock_tech(Unlocks.Trees)
	unlock_tech(Unlocks.Carrots)
	unlock_tech(Unlocks.Speed)
	unlock_tech(Unlocks.Watering)
	unlock_tech(Unlocks.Fertilizer)
	unlock_tech(Unlocks.Grass)
	unlock_tech(Unlocks.Trees)
	unlock_tech(Unlocks.Carrots)
	unlock_tech(Unlocks.Pumpkins)
	unlock_tech(Unlocks.Watering)
	unlock_tech(Unlocks.Cactus)
	unlock_tech(Unlocks.Cactus)
	unlock_tech(Unlocks.Dinosaurs)
	unlock_tech(Unlocks.Dinosaurs)
	unlock_tech(Unlocks.Mazes)
	unlock_tech(Unlocks.Leaderboard)
	s = get_time() - s
	d = s // 86400
	s -= d * 86400
	h = s // 3600
	s -= h * 3600
	m = s // 60
	s -= m * 60
	s = s // 1
	do_a_flip()
	quick_print("Leaderboard unlocked: " + str(d) + "d " + pad(h) + "h " + pad(m) + "m " + pad(s) + "s")

def unlock_tech(tech):
	ct = get_cost(tech)
	for c in ct:
		farm_item(c, ct[c])
	if not unlock(tech):
		unlock_tech(tech)
	pet_the_piggy()
	if tech == Unlocks.Expand:
		global ws
		global rws
		ws = get_world_size()
		rws = range(ws)

def pad(c):
	s = str(c)
	if len(s) <= 1:
		s = "0" + s
	return s

def farm_item(item, num):
	while num_items(item) < num:
		if item == Items.Hay:
			farm_grass()
		elif item == Items.Wood:
			if num_unlocked(Unlocks.Trees) > 0:
				farm_trees()
			else:
				farm_bushes()
		elif item == Items.Carrot:
			farm_carrots(num - num_items(item))
		elif item == Items.Pumpkin or item == Items.Weird_Substance:
			farm_pumpkins(num - num_items(item))
		elif item == Items.Cactus:
			farm_cactus(num - num_items(item))
		elif item == Items.Bone:
			farm_bones(((num - num_items(item)) // ((ws**2 - 1)**2)) * (ws**2 - 1) * 2**(num_unlocked(Unlocks.Dinosaurs) - 1) // 4 * 2)
		elif item == Items.Gold:
			farm_gold(num)

# === HELPERS PARALELOS ===

def _cria_faixa_sow(x_ini, x_fim, tam, to_harvest, water, entity):
	cols = []
	x = x_ini
	while x < x_fim:
		cols.append(x)
		x += 1
	def funcao():
		y = 0
		while y < tam:
			for x in cols:
				_move_to(x, y)
				_sow(to_harvest, water, entity)
			y += 1
	return funcao

def _paraleliza_sow(to_harvest, water, entity):
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
		tarefa = _cria_faixa_sow(x_ini, x_fim, tam, to_harvest, water, entity)
		d = spawn_drone(tarefa)
		if d:
			drones.append(d)
		else:
			tarefa()
		i += 1
	for d in drones:
		wait_for(d)

def _sow(to_harvest, water, entity):
	if to_harvest:
		if can_harvest():
			harvest()
	elif get_entity_type() != entity:
		if can_harvest():
			harvest()
	if get_ground_type() != _get_ground(entity):
		till()
	if water and num_unlocked(Unlocks.Watering) > 0 and get_ground_type() == Grounds.Soil:
		if get_water() < 0.5 and num_items(Items.Water) > 0:
			use_item(Items.Water)
	if get_entity_type() != entity:
		plant(entity)

def _get_ground(entity):
	if entity == Entities.Grass or entity == Entities.Bush:
		return Grounds.Grassland
	return Grounds.Soil

# === FARM FUNCTIONS ===

def farm_grass():
	_paraleliza_sow(True, False, Entities.Grass)

def farm_bushes():
	sow_tile(True, False, Entities.Bush)

def farm_trees():
	# arvores em xadrez: cada drone trata sua faixa
	tam = get_world_size()
	nd = max_drones()
	if nd < 1:
		nd = 1
	faixa = tam // nd
	if faixa < 1:
		faixa = 1
	def _cria_faixa_tree(x_ini, x_fim, tam):
		cols = []
		x = x_ini
		while x < x_fim:
			cols.append(x)
			x += 1
		def funcao():
			y = 0
			while y < tam:
				for x in cols:
					if (x + y) % 2 == 0:
						_move_to(x, y)
						_sow(True, True, Entities.Tree)
				y += 1
		return funcao
	drones = []
	i = 0
	while i < nd:
		x_ini = i * faixa
		if i == nd - 1:
			x_fim = tam
		else:
			x_fim = x_ini + faixa
		tarefa = _cria_faixa_tree(x_ini, x_fim, tam)
		d = spawn_drone(tarefa)
		if d:
			drones.append(d)
		else:
			tarefa()
		i += 1
	for d in drones:
		wait_for(d)

def farm_carrots(num):
	get_resources_for(Entities.Carrot, num // (2**(num_unlocked(Unlocks.Carrots) - 1)))
	_paraleliza_sow(True, True, Entities.Carrot)

def farm_pumpkins(num):
	get_resources_for(Entities.Pumpkin, num // (2*2**(num_unlocked(Unlocks.Pumpkins) - 1)))
	_paraleliza_sow(True, True, Entities.Pumpkin)
	# fertilizante
	if num_unlocked(Unlocks.Fertilizer) > 0 and num_items(Items.Fertilizer) > 0:
		tam = get_world_size()
		y = 0
		while y < tam:
			x = 0
			while x < tam:
				_move_to(x, y)
				if num_items(Items.Fertilizer) > 0:
					use_item(Items.Fertilizer)
				x += 1
			y += 1

def farm_cactus(num):
	get_resources_for(Entities.Cactus, num // (2**(num_unlocked(Unlocks.Cactus) - 1)))
	_paraleliza_sow(True, True, Entities.Cactus)
	# ordena em paralelo para bonus n²
	_ordena_cactus_paralelo()
	_move_to(0, 0)
	harvest()

def _cria_ordena_coluna(col, tam):
	def funcao():
		trocou = True
		while trocou:
			trocou = False
			j = 0
			while j < tam - 1:
				_move_to(col, j)
				v_norte = measure(North)
				if v_norte != None and measure() > v_norte:
					swap(North)
					trocou = True
				j += 1
	return funcao

def _cria_ordena_linha(lin, tam):
	def funcao():
		trocou = True
		while trocou:
			trocou = False
			j = 0
			while j < tam - 1:
				_move_to(j, lin)
				v_leste = measure(East)
				if v_leste != None and measure() > v_leste:
					swap(East)
					trocou = True
				j += 1
	return funcao

def _ordena_cactus_paralelo():
	tam = get_world_size()
	# fase 1: colunas em paralelo
	drones = []
	col = 0
	while col < tam:
		d = spawn_drone(_cria_ordena_coluna(col, tam))
		if d:
			drones.append(d)
		else:
			_cria_ordena_coluna(col, tam)()
		col += 1
	for d in drones:
		wait_for(d)
	# fase 2: linhas em paralelo
	drones = []
	lin = 0
	while lin < tam:
		d = spawn_drone(_cria_ordena_linha(lin, tam))
		if d:
			drones.append(d)
		else:
			_cria_ordena_linha(lin, tam)()
		lin += 1
	for d in drones:
		wait_for(d)
	# fase 3: colunas novamente (shearsort converge)
	passes = tam // 2
	if passes < 1:
		passes = 1
	p = 0
	while p < passes:
		drones = []
		col = 0
		while col < tam:
			d = spawn_drone(_cria_ordena_coluna(col, tam))
			if d:
				drones.append(d)
			else:
				_cria_ordena_coluna(col, tam)()
			col += 1
		for d in drones:
			wait_for(d)
		p += 1

def farm_bones(num):
	# Hamiltoniano serpentinado: percorre n²-1 celulas sem cruzar a cauda
	tam = get_world_size()
	get_resources_for(Entities.Apple, num // (2**(num_unlocked(Unlocks.Cactus) - 1)))
	clear()
	change_hat(Hats.Dinosaur_Hat)
	# serpentina: linha par vai East, linha impar vai West
	y = 0
	crescendo = True
	while crescendo:
		if y % 2 == 0:
			x = 0
			while x < tam - 1:
				if not move(East):
					change_hat(Hats.Straw_Hat)
					crescendo = False
					break
				x += 1
		else:
			x = tam - 1
			while x > 0:
				if not move(West):
					change_hat(Hats.Straw_Hat)
					crescendo = False
					break
				x -= 1
		if crescendo:
			if not move(North):
				change_hat(Hats.Straw_Hat)
				crescendo = False
			else:
				y += 1

def farm_gold(limit):
	global l
	global substance
	global currentDirection
	l = limit
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	clear()
	while num_items(Items.Gold) < l and num_items(Items.Weird_Substance) >= substance:
		currentDirection = North
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, substance)
		search_maze()
	clear()
	if not num_items(Items.Gold) >= l:
		farm_item(Items.Weird_Substance, (l - num_items(Items.Gold)) // (ws**2 // substance))

def sow_tile(to_harvest, water, entity):
	if (to_harvest and can_harvest()) or get_entity_type() != entity:
		harvest()
	if get_ground_type() != _get_ground(entity):
		till()
	if water and num_unlocked(Unlocks.Watering) > 0 and get_ground_type() == Grounds.Soil:
		while get_water() < 0.5 and num_items(Items.Water) > 0:
			use_item(Items.Water)
	if get_entity_type() != entity:
		plant(entity)

def get_resources_for(item, nb):
	nb_real = nb
	if nb_real < ws * ws:
		nb_real = ws * ws
	ci = get_cost(item)
	for c in ci:
		if num_items(c) < ci[c] * nb_real:
			farm_item(c, ci[c] * nb_real)

def search_maze():
	global currentDirection
	global l
	while num_items(Items.Gold) < l and num_items(Items.Weird_Substance) >= substance:
		while get_entity_type() == Entities.Hedge:
			if move(rightOf[currentDirection]):
				currentDirection = rightOf[currentDirection]
			elif move(currentDirection):
				pass
			elif move(leftOf[currentDirection]):
				currentDirection = leftOf[currentDirection]
			else:
				currentDirection = oppositeOf[currentDirection]
				move(currentDirection)
		if get_entity_type() == Entities.Treasure:
			harvest()
			clear()
			plant(Entities.Bush)
			use_item(Items.Weird_Substance, substance)
			currentDirection = North

if num_unlocked(Unlocks.Speed) == 0 and num_unlocked(Unlocks.Plant) == 0:
	slowest_automation()
else:
	print("You need to call this script")
	print("from a 'leaderboard_run' or 'simulate'")
