extends Area2D
class_name SlowFall

@onready var player: PlayerBot = get_node("/root/World/PlayerBot")
@onready var collision_shape: CollisionShape2D = $CollisionShape2D 
@onready var timer: Timer = $Timer
@onready var item: Sprite2D = get_node("/root/World/CanvasLayerHud/SlowFallSprite")
@onready var slow_fall_image = preload("res://power-ups/slow_fall.png")
 
var power_up_time = 15

func has_collided():
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 0, 0.1)
	call_deferred("disable_collision")  # Adia a chamada para desativar a colisão
	set_collision_layer(0)  
	timer.start(power_up_time)
	player.slow_fall_power_up = true
	item.texture = slow_fall_image
	

func disable_collision():
	collision_shape.disabled = true  


func _on_timer_timeout():
	player.slow_fall_power_up = false
	item.texture = null
	queue_free()
