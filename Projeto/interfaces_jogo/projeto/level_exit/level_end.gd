extends Area2D
class_name level_end


func _on_body_entered_lvl1(body):
	# load next level
	get_tree().change_scene_to_file("res://level/level2.tscn");
	# get_tree().call_deferred("change_scene_to_file", "res://level_exit/level_clear.tscn")
	
func _on_body_entered_lvl2(body):
	# load next level
	get_tree().change_scene_to_file("res://level/level3.tscn");
	# get_tree().call_deferred("change_scene_to_file", "res://level_exit/level_clear.tscn")
	
func _on_body_entered_lvl3(body):
	# load next level
	get_tree().change_scene_to_file("res://level/level4.tscn");
	# get_tree().call_deferred("change_scene_to_file", "res://level_exit/level_clear.tscn")
	
func _on_body_entered_lvl4(body):
	# load next level
	get_tree().change_scene_to_file("res://level/level5.tscn");
	# get_tree().call_deferred("change_scene_to_file", "res://level_exit/level_clear.tscn")
	
func _on_body_entered_lvl5(body):
	# load next level
	get_tree().change_scene_to_file("res://level/level6.tscn");
	#get_tree().call_deferred("change_scene_to_file", "res://level_exit/level_clear.tscn")
	
func _on_body_entered_lvl6(body):
	# load next level
	#get_tree().change_scene_to_file("res://level/level2.tscn");
	get_tree().call_deferred("change_scene_to_file", "res://level_exit/level_clear.tscn")
