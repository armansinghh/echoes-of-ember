extends Area2D

@onready var sprite: AnimatedSprite2D = $Sprite

func _ready() -> void:
	sprite.play()
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
	if body.has_method("respawn"):
		body.respawn.call_deferred()
