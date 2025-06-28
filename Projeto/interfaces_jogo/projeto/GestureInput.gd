extends Node

const UDP_IP = "127.0.0.1"
const UDP_PORT = 65432
var udp := PacketPeerUDP.new()
var current_input_states := {
	"Space": false,
	"ui_right": false,
	"ui_left": false
}

func _ready():
	setup_udp()

func setup_udp():
	if udp.bind(UDP_PORT, UDP_IP) != OK:
		print("Erro ao vincular socket UDP")
		await get_tree().create_timer(2.0).timeout
		setup_udp()
	else:
		print("UDP ouvindo em:", UDP_IP, UDP_PORT)

func _process(_delta):
	while udp.get_available_packet_count() > 0:
		var packet = udp.get_packet()
		var message = packet.get_string_from_utf8()
		handle_gesture_message(message)

func handle_gesture_message(message: String):
	print("Recebido:", message)  # Debug
	
	match message:
		"space_down":
			set_input_state("Space", true)
		"space_up":
			set_input_state("Space", false)
		"right_down":
			set_input_state("ui_right", true)
		"right_up":
			set_input_state("ui_right", false)
		"left_down":
			set_input_state("ui_left", true)
		"left_up":
			set_input_state("ui_left", false)
		_:
			print("Mensagem desconhecida:", message)

func set_input_state(action_name: String, is_pressed: bool):
	if current_input_states.has(action_name):
		var old_state = current_input_states[action_name]
		if old_state != is_pressed:
			current_input_states[action_name] = is_pressed
			emit_signal("gesture_input_changed", action_name, is_pressed)

signal gesture_input_changed(action_name: String, is_pressed: bool)

func _exit_tree():
	udp.close()
