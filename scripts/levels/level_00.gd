extends Node2D

@onready var win_label: Label = $UI/WinLabel

func _ready() -> void:
	$Lantern.reached.connect(_on_lantern_reached)

func _on_lantern_reached() -> void:
	win_label.show()
	$Player.set_physics_process(false)
