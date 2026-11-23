extends CanvasLayer

@onready var resume_button: Button = $Buttons/ResumeButton
@onready var menu_button: Button = $Buttons/MenuButton

func _ready() -> void:
	hide()
	resume_button.pressed.connect(resume)
	menu_button.pressed.connect(_on_menu)

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause"):
		if get_tree().paused:
			resume()
		else:
			pause()
		get_viewport().set_input_as_handled()

func pause() -> void:
	get_tree().paused = true
	show()
	resume_button.grab_focus()

func resume() -> void:
	get_tree().paused = false
	hide()

func _on_menu() -> void:
	get_tree().paused = false
	SceneTransition.change_scene("res://scenes/main_menu.tscn")
