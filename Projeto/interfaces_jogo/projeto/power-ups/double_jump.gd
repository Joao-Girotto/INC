extends Area2D
class_name DoubleJump

@onready var player: PlayerBot = get_node("/root/World/PlayerBot")
@onready var collision_shape: CollisionShape2D = $CollisionShape2D 
@onready var timer: Timer = $Timer
@onready var item: Sprite2D = get_node("/root/World/CanvasLayerHud/DoubleJumpSprite")
@onready var double_jump_image = preload("res://power-ups/paw_cat_double_jump.png")
 
var power_up_time = 15

func has_collided():
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 0, 0.1)
	call_deferred("disable_collision")  # Adia a chamada para desativar a colisão
	set_collision_layer(0) 
	timer.start(power_up_time)
	player.double_jump_power_up = true
	item.texture = double_jump_image

func disable_collision():
	collision_shape.disabled = true  


func _on_timer_timeout():
	player.double_jump_power_up = false
	item.texture = null
	queue_free()
