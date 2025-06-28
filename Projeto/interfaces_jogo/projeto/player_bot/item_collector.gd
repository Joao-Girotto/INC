extends Area2D
class_name ItemCollector

var _total_items: int = 0
@onready var player: PlayerBot = get_node("/root/World/PlayerBot")
@onready var collect: AudioStreamPlayer =  $"../CollectSFX"
var power_up_time = 10.0
signal item_collected(item: Item)

func _on_area_entered(item) -> void:
	if item is Item:
		item_collected.emit(item)
		_total_items += item.get_value()
		gc.update_hud_items(_total_items)
		collect.play()
		item.queue_free()
	elif item is KeyItem:
		player.has_key = true
		item.get_key()
		collect.play()
	else:
		item.has_collided()	
		collect.play()
