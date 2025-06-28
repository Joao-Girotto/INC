extends Area2D
class_name Item

@onready var _player: AnimationPlayer = $AnimationPlayer

@export var value: int = 5

func _ready() -> void:
	var offset: int = int(global_position.x) % 10
	_player.seek( (_player.current_animation_length / 10) * offset)
	

func get_value() -> int:
	return value


func _on_collision_shape_2d_ready() -> void:
	pass 
