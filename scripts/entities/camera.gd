extends Camera2D

@export var speed := 3.5       # ease-out strength
@export var overshoot := 3.0   # px past the target; lower = softer stop

@onready var target: Node2D = get_parent()

var cam_pos: Vector2

func _ready() -> void:
	top_level = true
	physics_interpolation_mode = Node.PHYSICS_INTERPOLATION_MODE_OFF
	snap_to_target()

func snap_to_target() -> void:
	cam_pos = target.global_position
	global_position = _snap(cam_pos)

func _process(delta: float) -> void:
	var weight: float = 1.0 - exp(-speed * delta)
	var goal: Vector2 = target.global_position
	cam_pos.x = _lerp_overshoot(cam_pos.x, goal.x, weight, overshoot)
	cam_pos.y = _lerp_overshoot(cam_pos.y, goal.y, weight, overshoot)
	global_position = _snap(cam_pos)

func _lerp_overshoot(from: float, to: float, weight: float, over: float) -> float:
	var d: float = to - from
	if absf(d) < 0.001:
		return to
	var s: float = signf(d)
	var l: float = lerpf(from, to + over * s, weight)
	return minf(l, to) if s > 0.0 else maxf(l, to)

func _snap(p: Vector2) -> Vector2:
	var s: float = _screen_scale()
	return (p * s).round() / s

func _screen_scale() -> float:
	var win := get_window()
	var base := Vector2(win.content_scale_size)
	if base.x <= 0.0 or base.y <= 0.0:
		return 1.0
	return maxf(minf(win.size.x / base.x, win.size.y / base.y), 1.0)
