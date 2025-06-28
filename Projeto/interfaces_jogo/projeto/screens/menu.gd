extends Control

func _on_start_button_pressed():
	get_tree().change_scene_to_file("res://level/level1.tscn");


func _on_instructions_button_pressed():
	get_tree().change_scene_to_file("res://screens/instructions.tscn")


func _on_credits_button_pressed():
	get_tree().change_scene_to_file("res://screens/credits.tscn")


func _on_quit_button_pressed():
	get_tree().quit()
