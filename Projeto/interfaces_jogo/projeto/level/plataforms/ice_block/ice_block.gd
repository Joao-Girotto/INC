extends AnimatableBody2D

@onready var animated_sprite: AnimatedSprite2D = get_node("/root/World/PlayerBot/AnimatedSprite2D")
@export var slide_factor := 40.0 
var player_velocity := Vector2.ZERO  

func _ready():
	set_physics_process(true)

func has_collided_with(collider: CharacterBody2D):
	if collider.is_in_group("Player"):
		player_velocity = collider.velocity
	
		if collider.scale.x > 0:
		#if collider.global_position.x < global_position.x:
			player_velocity.x = -slide_factor  
		else:
			player_velocity.x = slide_factor 
		animated_sprite.play("idle")
		collider.velocity = player_velocity
 
