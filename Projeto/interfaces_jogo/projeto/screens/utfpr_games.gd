extends Control

@onready var timer: Timer = $Timer

func _ready():
	timer.start(3)

func _on_timer_timeout():
	get_tree().change_scene_to_file("res://screens/menu.tscn")
	music.play_music()
