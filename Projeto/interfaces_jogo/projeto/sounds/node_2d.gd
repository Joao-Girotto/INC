extends Node2D


func _ready():
	pass 


func play_music():
	$AudioStreamPlayer.play()


func stop_music():
	$AudioStreamPlayer.stop()
