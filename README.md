Central_system.v1

this Central_system, based on OCPP protocol.

1. Use a client connect to this central_system

2. if Client send the following functions based on OCPP protocols, this central_system can  reply relatively responses. (all the parameters in these functions should be initialized before using)
	boot_notification
	authorize
	heart_beat
	start_transaction
	stop_transaction
	meter_value
	status_notification
	data_transfer

3.Central_system can send the following functions to it's clients:
	send_clear_cache_request
	send_remote_start_transaction
	send_remote_stop_transaction
	set_charging_profile
	clear_charging_profile
	cancel_reservation
	change_availability
	get_configuration
	change_configuration
	data_transfer
	get_local_list_version
	send_local_list
	reset
	unlock_connector
	update_firmware
	
4. two data folder store all the data that transfer between central_system and client, including  the original scommands,local time and function name.
    (1).dataFromCp2Server:  initial form client, (req, con)
    (2).dataFromServer2Cp:  initial form server, (req, con)

5.if you want to change the max current, please set the current value you want, then you can send to client


    

