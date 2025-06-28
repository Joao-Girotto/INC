extends Node2D
class_name GameInit

@onready var _camera: CameraShake = $PlayerBot/Camera2D

func _ready() -> void:
	_camera.init_camera_limits(_get_map_bounds($TileMap))
	music.stop_music()


func _get_map_bounds(tilemap: TileMap) -> Rect2:
	var map_rect: Rect2 = tilemap.get_used_rect()
	var cell_size: float = tilemap.tile_set.tile_size.x * tilemap.scale.x
	
	var pos := map_rect.position * cell_size
	var size:= map_rect.size * cell_size
	
	return Rect2(pos, size)


func _on_body_entered_lvl1(_body):
	# load next level
	#get_tree().change_scene_to_file("res://level/level2.tscn");
	get_tree().call_deferred("change_scene_to_file", "res://level/level2.tscn")

func _on_body_entered_lvl2(_body):
	# load next level
	#get_tree().change_scene_to_file("res://level/level3.tscn");
	get_tree().call_deferred("change_scene_to_file", "res://level/level3.tscn")
	
func _on_body_entered_lvl3(_body):
	# load next level
	#get_tree().change_scene_to_file("res://level/level4.tscn");
	get_tree().call_deferred("change_scene_to_file", "res://level/level4.tscn")
	
func _on_body_entered_lvl4(_body):
	# load next level
	#get_tree().change_scene_to_file("res://level/level5.tscn");
	get_tree().call_deferred("change_scene_to_file", "res://level/level5.tscn")
	
func _on_body_entered_lvl5(_body):
	# load next level
	#get_tree().change_scene_to_file("res://level/level6.tscn");
	get_tree().call_deferred("change_scene_to_file", "res://level/level6.tscn")


func _on_body_entered_lvl6(body):
	get_tree().call_deferred("change_scene_to_file", "res://level_exit/level_clear.tscn")
