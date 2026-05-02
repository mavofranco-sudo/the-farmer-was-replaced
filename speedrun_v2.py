ws = get_world_size()
rws = range(ws)
leftOf = {North:West, East:North, South:East, West:South}
rightOf = {North:East, East:South, South:West, West:North}
oppositeOf = {North:South, East:West, South:North, West:East}
currentDirection = North
l = -1
substance = -1

def pad(c):
	s = str(c)
	if len(s) <= 1:
		s = "0" + s
	return s

# === NAVEGACAO ===
def _vai(x, y):
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

# === PARALELISMO ===
def _spawn(fn):
	d = spawn_drone(fn)
	if d:
		return d
	fn()
	return None

def _wait(drones):
	for d in drones:
		if d:
			wait_for(d)

def _faixas(fn_cria):
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
		cols = []
		x = x_ini
		while x < x_fim:
			cols.append(x)
			x += 1
		drones.append(_spawn(fn_cria(cols, tam)))
		i += 1
	_wait(drones)

# === SOW PARALELO ===
def _get_ground(entity):
	if entity == Entities.Grass or entity == Entities.Bush:
		return Grounds.Grassland
	return Grounds.Soil

def _sow_cell(entity, water, harvest_first):
	if harvest_first:
		if can_harvest():
			harvest()
	elif get_entity_type() != entity:
		if can_harvest():
			harvest()
	if get_ground_type() != _get_ground(entity):
		till()
	if water and num_unlocked(Unlocks.Watering) > 0:
		if get_ground_type() == Grounds.Soil:
			if get_water() < 0.5 and num_items(Items.Water) > 0:
				use_item(Items.Water)
	if get_entity_type() != entity:
		plant(entity)

def _cria_sow(cols, tam, entity, water, harvest_first):
	def fn():
		y = 0
		while y < tam:
			for x in cols:
				_vai(x, y)
				_sow_cell(entity, water, harvest_first)
			y += 1
	return fn

def _sow_paralelo(entity, water, harvest_first):
	def fn_cria(cols, tam):
		return _cria_sow(cols, tam, entity, water, harvest_first)
	_faixas(fn_cria)

# === FARMS ===
def farm_grass():
	_sow_paralelo(Entities.Grass, False, True)

def farm_bushes():
	_sow_cell(Entities.Bush, False, True)

def farm_trees():
	tam = get_world_size()
	nd = max_drones()
	if nd < 1:
		nd = 1
	faixa = tam // nd
	if faixa < 1:
		faixa = 1
	def _cria_tree(cols, tam):
		def fn():
			y = 0
			while y < tam:
				for x in cols:
					if (x + y) % 2 == 0:
						_vai(x, y)
						_sow_cell(Entities.Tree, True, True)
				y += 1
		return fn
	_faixas(_cria_tree)

def farm_carrots(num):
	_get_res_for(Entities.Carrot, num // (2**(num_unlocked(Unlocks.Carrots) - 1)))
	_sow_paralelo(Entities.Carrot, True, True)

def farm_pumpkins(num):
	_get_res_for(Entities.Pumpkin, num // (2 * 2**(num_unlocked(Unlocks.Pumpkins) - 1)))
	_sow_paralelo(Entities.Pumpkin, True, True)
	if num_unlocked(Unlocks.Fertilizer) > 0:
		tam = get_world_size()
		y = 0
		while y < tam:
			x = 0
			while x < tam:
				_vai(x, y)
				if num_items(Items.Fertilizer) > 0:
					use_item(Items.Fertilizer)
				x += 1
			y += 1

def farm_cactus(num):
	_get_res_for(Entities.Cactus, num // (2**(num_unlocked(Unlocks.Cactus) - 1)))
	_sow_paralelo(Entities.Cactus, True, True)
	_ordena_cactus()
	_vai(0, 0)
	harvest()

def farm_bones(num):
	_get_res_for(Entities.Apple, num)
	clear()
	change_hat(Hats.Dinosaur_Hat)
	tam = get_world_size()
	crescendo = True
	y = 0
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
		_search_maze()
	clear()
	if num_items(Items.Gold) < l:
		farm_item(Items.Weird_Substance, (l - num_items(Items.Gold)) // (ws**2 // substance))

def _search_maze():
	global currentDirection
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

# === ORDENACAO CACTUS PARALELA ===
def _cria_ord_col(col, tam):
	def fn():
		trocou = True
		while trocou:
			trocou = False
			j = 0
			while j < tam - 1:
				_vai(col, j)
				vn = measure(North)
				if vn != None and measure() > vn:
					swap(North)
					trocou = True
				j += 1
	return fn

def _cria_ord_lin(lin, tam):
	def fn():
		trocou = True
		while trocou:
			trocou = False
			j = 0
			while j < tam - 1:
				_vai(j, lin)
				ve = measure(East)
				if ve != None and measure() > ve:
					swap(East)
					trocou = True
				j += 1
	return fn

def _ordena_cactus():
	tam = get_world_size()
	# colunas paralelas
	drones = []
	c = 0
	while c < tam:
		drones.append(_spawn(_cria_ord_col(c, tam)))
		c += 1
	_wait(drones)
	# linhas paralelas
	drones = []
	r = 0
	while r < tam:
		drones.append(_spawn(_cria_ord_lin(r, tam)))
		r += 1
	_wait(drones)
	# colunas de novo (shearsort)
	p = 0
	passes = tam // 2
	if passes < 1:
		passes = 1
	while p < passes:
		drones = []
		c = 0
		while c < tam:
			drones.append(_spawn(_cria_ord_col(c, tam)))
			c += 1
		_wait(drones)
		p += 1

# === RECURSOS ===
def _get_res_for(entity, nb):
	tam = get_world_size()
	if nb < tam * tam:
		nb = tam * tam
	ci = get_cost(entity)
	for c in ci:
		needed = ci[c] * nb
		if num_items(c) < needed:
			farm_item(c, needed)

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
			n2 = ws * ws - 1
			ciclos_necessarios = (num - num_items(item) + n2 - 1) // n2
			farm_bones(ciclos_necessarios)
		elif item == Items.Gold:
			farm_gold(num)

# === UNLOCK ===
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

if num_unlocked(Unlocks.Speed) == 0 and num_unlocked(Unlocks.Plant) == 0:
	slowest_automation()
else:
	print("You need to call this script")
	print("from a 'leaderboard_run' or 'simulate'")
