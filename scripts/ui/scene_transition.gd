extends CanvasLayer

const FADE_TIME := 0.3

@onready var fade: ColorRect = $Fade

var busy := false

func change_scene(path: String) -> void:
	if busy:
		return
	busy = true
	fade.mouse_filter = Control.MOUSE_FILTER_STOP
	var tween := create_tween()
	tween.tween_property(fade, "modulate:a", 1.0, FADE_TIME)
	await tween.finished
	get_tree().paused = false
	get_tree().change_scene_to_file(path)
	await get_tree().process_frame
	tween = create_tween()
	tween.tween_property(fade, "modulate:a", 0.0, FADE_TIME)
	await tween.finished
	fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	busy = false
