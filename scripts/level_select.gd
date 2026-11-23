extends Control

const LEVELS := [
	"res://scenes/level_00.tscn",
	"res://scenes/level_01.tscn",
	"res://scenes/level_02.tscn",
	"res://scenes/level_03.tscn",
	"res://scenes/level_04.tscn",
	"res://scenes/level_05.tscn",
]

@onready var grid: GridContainer = $Levels
@onready var back_button: Button = $BackButton

func _ready() -> void:
	var first_playable: Button = null
	for i in LEVELS.size():
		var path: String = LEVELS[i]
		var button := Button.new()
		button.text = str(i)
		button.custom_minimum_size = Vector2(64, 64)
		if ResourceLoader.exists(path):
			button.pressed.connect(func(): SceneTransition.change_scene(path))
			if first_playable == null:
				first_playable = button
		else:
			button.disabled = true
		grid.add_child(button)

	back_button.pressed.connect(_on_back)
	if first_playable:
		first_playable.grab_focus()

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		_on_back()

func _on_back() -> void:
	SceneTransition.change_scene("res://scenes/main_menu.tscn")
