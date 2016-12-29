# emailsender

####System Requirements
- Python 2.7

####To run
- python sendmail.py \<config.json\>


{
	"message": {
		"from"			: "sender@sourcedomain.com",
		"to"			: "recipient@targetdomain.com",
		"subject"		: "",
		"attachment"	: false,
		"attachment_id"	: 0
	},

	"smtp_config": {
		"smtp_server"	: "smtp.server.com",
		"smtp_port"		: 25,
		"smtp_use_ssl"	: false,
		"smtp_username"	: "",
		"smtp_password"	: ""
	},

	"batch_config": {
		"number_of_emails": 1,
		"min_wait": 0,
		"max_wait": 0,
		"randomize_senders": false,
		"senders_override": [],
		"randomize_attachements": false
	}
}
