extends AnimatableBody2D

@onready var animation := $AnimationPlayer as AnimationPlayer
@onready var respawn_timer := $Timer as Timer
@onready var respawn_position := global_position

@export var reset_timer := 5.0

var is_triggered := false
@onready var collision_shape := $CollisionShape2D as CollisionShape2D 
@onready var texture := $Sprite2D

func _ready():
	set_physics_process(false)
	
func has_collided_with(collider: CharacterBody2D):
	if !is_triggered:
		is_triggered = true
		animation.play("shake")    

func _on_animation_player_animation_finished(anim_name):
	var tween = create_tween()
	$GPUParticles2D.emitting = true
	tween.tween_property(self, "modulate:a", 0, 0.4)
	collision_shape.disabled = true
	respawn_timer.start(reset_timer)

func _on_timer_timeout():
	global_position = respawn_position
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 1, 0.4)
	collision_shape.disabled = false
	
	is_triggered = false
