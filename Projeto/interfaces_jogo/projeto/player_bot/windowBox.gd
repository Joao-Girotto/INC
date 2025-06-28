extends Area2D
@onready var player: PlayerBot = get_node("/root/World/PlayerBot")
@onready var key: Sprite2D = get_node("/root/World/CanvasLayerHud/Key")

func _on_area_entered(area):
	if area.is_in_group("window"): 
		if player.has_key:
			var window_area = area as Area2D 
			if window_area and not window_area.window_is_locked: 
				for window in get_tree().get_nodes_in_group("window"):
					if window != window_area: 
						if window.id == window_area.id:
							window_area.lock_window() 
							player. global_position = window.global_position  
							player.has_key = false
							key.texture = null
