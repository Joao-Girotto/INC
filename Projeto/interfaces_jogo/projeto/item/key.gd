extends Area2D
class_name KeyItem

@onready var key: Sprite2D = get_node("/root/World/CanvasLayerHud/Key")
@onready var key_image = preload("res://item/Key.png")
@onready var animation = $AnimationPlayer

func _process(_delta):
	animation.play("idle")
	
func get_key():
	key.texture = key_image
	queue_free()
