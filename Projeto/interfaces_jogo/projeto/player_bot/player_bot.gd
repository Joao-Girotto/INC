extends CharacterBody2D
class_name PlayerBot

const SPEED: float = 100
const ACCELERATION: float = 800
const FRICTION: float = 900
const JUMP_VELOCITY: float = -1400
const JUMP_VELOCITY_MIN: float = JUMP_VELOCITY / 3
const MAX_JUMP_HOLD: int = 1500
const DOUBLE_JUMP_FORCE: int = 500
const MAX_JUMP_FORCE: float = 0.7 

@onready var _animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var jump_sfx: AudioStreamPlayer = $JumpSFX 
@onready var jump_power_bar: ProgressBar = get_node("/root/World/PlayerBot/ProgressBar") # Certifique-se de que o caminho está correto
@onready var gesture_input: Node = $GestureInput # Caminho para o nó do seu script de input de gestos

const DEBUG: bool = false
var jump_time: float = 0
var _gravity = 980 * 2
var _direction = 1
var _is_double_jump: bool = false
var _start_posisition: Vector2
var double_jump_power_up: bool = false
var slow_fall_power_up: bool = false
var is_shocked: bool = false
var has_key: bool = false

# Variáveis para simular o estado dos inputs
var _gesture_jump_pressed: bool = false
var _gesture_jump_just_pressed: bool = false
var _gesture_jump_just_released: bool = false
var _gesture_left_pressed: bool = false
var _gesture_right_pressed: bool = false

func _ready():
	_start_posisition = position
	if not jump_power_bar:
		print("Erro: ProgressBar não encontrado.")
	else:
		jump_power_bar.visible = false 
	
	if gesture_input:
		gesture_input.connect("gesture_input_changed", Callable(self, "_on_gesture_input_changed"))
	else:
		print("Erro: Nó GestureInput não encontrado.")


func _on_gesture_input_changed(action_name: String, is_pressed: bool):
	match action_name:
		"Space":
			_gesture_jump_just_pressed = (is_pressed and not _gesture_jump_pressed)
			_gesture_jump_just_released = (not is_pressed and _gesture_jump_pressed)
			_gesture_jump_pressed = is_pressed
		
		"ui_left":
			_gesture_left_pressed = is_pressed
		
		"ui_right":
			_gesture_right_pressed = is_pressed

func _process(delta: float) -> void:
	# Lógica de gravidade (permanece a mesma)
	if not is_on_floor():
		if(slow_fall_power_up or DEBUG):
			velocity.y += _gravity * delta / 3
			if(velocity.y <= 0):
				velocity.y += _gravity * delta / 2
		else:
			velocity.y += _gravity * delta
	
	var input: float = 0.0
	if _gesture_left_pressed:
		input += 1.0
	if _gesture_right_pressed:
		input -= 1.0


	if _gesture_jump_just_pressed:
		jump_time = Time.get_ticks_msec()
		if(is_on_floor()):
			jump_power_bar.visible = true 
		
		if(not is_on_floor() and ((not _is_double_jump and double_jump_power_up) or DEBUG)):
			velocity.y = JUMP_VELOCITY * 0.5
			velocity.x = input * JUMP_VELOCITY_MIN * 0.5 * -1
			_is_double_jump = true
	
	if _gesture_jump_pressed: 
		var time_now = Time.get_ticks_msec() - jump_time
		var jump_force = min(time_now, MAX_JUMP_HOLD) / MAX_JUMP_HOLD * MAX_JUMP_FORCE
		if(is_on_floor()):
			jump_power_bar.visible = true
		if jump_power_bar:
			jump_power_bar.value = jump_force / MAX_JUMP_FORCE * 100.0
		
	if _gesture_jump_just_released: 
		if jump_power_bar:
			jump_power_bar.value = 0   
			jump_power_bar.visible = false   
		
		if is_on_floor():
			var time_now = Time.get_ticks_msec() - jump_time
			var jump_force = min(time_now, MAX_JUMP_HOLD) / MAX_JUMP_HOLD * MAX_JUMP_FORCE

			velocity.y = JUMP_VELOCITY * jump_force
			velocity.x = input * JUMP_VELOCITY_MIN * jump_force 

			_is_double_jump = false
			jump_sfx.play()

	_gesture_jump_just_pressed = false
	_gesture_jump_just_released = false
	
	if input:
		print("input")
		if is_on_floor():
			velocity.x = move_toward(velocity.x, 0 * SPEED, ACCELERATION * delta) 
			_direction = sign(input)
		else:
			if velocity.y <= 0:
				velocity.x = move_toward(velocity.x, input * 250, ACCELERATION * delta * 2)
			_direction = sign(input)
	else:
		velocity.x = move_toward(velocity.x, 0, FRICTION * delta)
	
	if velocity.y > 0:
		velocity.y = clamp(velocity.y, 0, 800)
	
	move_and_slide()
	_animate_player()
	
	for platforms in get_slide_collision_count():
		var collision = get_slide_collision(platforms)
		if collision.get_collider().has_method("has_collided_with"):
			collision.get_collider().has_collided_with(self)   

func _animate_player():
	if is_shocked == true:
		_animated_sprite.play("shock")
	elif is_on_floor():
		if velocity.x != 0:
			_animated_sprite.play("run")
		else:
			_animated_sprite.play("idle")
	else:
		if velocity.y < 0:
			_animated_sprite.play("jump")
		else:
			_animated_sprite.play("fall")

	_animated_sprite.scale.x = _direction
