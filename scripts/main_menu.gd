extends Control

@onready var play_button: Button = $Buttons/PlayButton
@onready var options_button: Button = $Buttons/OptionsButton
@onready var quit_button: Button = $Buttons/QuitButton

func _ready() -> void:
	play_button.pressed.connect(_on_play)
	options_button.pressed.connect(_on_options)
	quit_button.pressed.connect(get_tree().quit)
	play_button.grab_focus()

func _on_play() -> void:
	SceneTransition.change_scene("res://scenes/level_select.tscn")

func _on_options() -> void:
	pass # placeholder, like your pygame version
