extends CharacterBody2D

const MAX_SPEED := 200.0
const ACCEL := 1200.0
const FRICTION := 1000.0
const GRAVITY := 800.0
const JUMP_VELOCITY := -300.0
const FALL_LIMIT := 560.0

@onready var ember: AnimatedSprite2D = $Ember
@onready var fire: AnimatedSprite2D = $Fire

var spawn_position: Vector2

func _ready() -> void:
	spawn_position = global_position
	fire.play("flicker")

func _physics_process(delta: float) -> void:
	var dir := Input.get_axis("move_left", "move_right")

	if dir != 0.0:
		velocity.x = move_toward(velocity.x, dir * MAX_SPEED, ACCEL * delta)
		ember.flip_h = dir < 0.0
		fire.position = Vector2(-19.0 if dir < 0.0 else 20.0, -12.0)
		if ember.animation != "walk" or not ember.is_playing():
			ember.play("walk")
	else:
		velocity.x = move_toward(velocity.x, 0.0, FRICTION * delta)
		ember.stop()
		ember.frame = 0

	velocity.y += GRAVITY * delta

	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	move_and_slide()

	if global_position.y > FALL_LIMIT:
		respawn()

func respawn() -> void:
	global_position = spawn_position
	velocity = Vector2.ZERO
