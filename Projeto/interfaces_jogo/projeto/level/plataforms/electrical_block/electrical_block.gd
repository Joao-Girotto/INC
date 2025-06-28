extends AnimatableBody2D

@onready var player: PlayerBot = get_node("/root/World/PlayerBot")
@onready var timer: Timer = $Timer
@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var animation : AnimationPlayer = $AnimationPlayer

var knockback_force:= Vector2(500, 200)
var shocked: bool = false

func _process(delta):
	if shocked == false:
		animation.play("activate")
	else:
		animated_sprite.play("activate")
		shocked = true


func has_collided_with(collider: CharacterBody2D):
	if collider.is_in_group("Player") and shocked:
		#player.velocity = knockback_force 
		
		if player.global_position.x < global_position.x:
			# Aplica o knockback para a esquerda
			player.velocity = Vector2(-knockback_force.x, -knockback_force.y)
		else:
			# Aplica o knockback para a direita
			player.velocity = knockback_force 
		
		player.is_shocked = true
		timer.start(0.7)

func _on_timer_timeout():
	player.is_shocked = false


func _on_animation_player_animation_finished(anim_name):
	animation.stop()
	shocked = true


func _on_animated_sprite_2d_animation_looped():
	animated_sprite.stop()
	shocked = false
