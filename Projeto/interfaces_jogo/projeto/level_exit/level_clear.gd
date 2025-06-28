extends Node2D


# Called when the node enters the scene tree for the first time.
func _ready():
	$LabelScore.text = "Score: %04d" % gc.score
