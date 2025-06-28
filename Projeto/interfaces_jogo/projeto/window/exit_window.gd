extends Area2D
class_name WindowExitClass

static var window_count: int = 0

# ID único da janela
@export var id: int = 0
var window_is_locked: bool = false

func _ready():
	# Incrementa o contador global e atribui o ID à janela atual
	id = window_count
	window_count += 1
