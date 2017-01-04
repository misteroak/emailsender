# emailsender

####System Requirements
- Python 2.7

####To run
- ```python sendmail.py <config.json>```

####Configuration file settings (JSON), see [example](https://github.com/misteroak/emailsender/blob/master/config.json)
\* - denotes a mandatory fields

- **message**
  - **from** (string)*: sender's email address
  - **to** (string)*: recipient's email address
  - **subject** (string)*: subject line
  - **attachement** (boolean)*: whether to attach a file or not. Files are looked up in a directory named 'attachments' in the same folder where the script is executed. Ignored if ```batch_config->randomize_attachements``` is true.
  - **attachment_id** (integrer): the index of the file to use as attachement. Ignored if ```message->attachemnt``` is false.

- **smtp_config**
  - **smtp_server** (string)\*: ip/hostname of the smtp server from which to send the email
  - **smtp_port** (integer)\*: target port to use
  - **smtp_use_ssl** (boolean)\* : whether to use ssl or not
  - **smtp_username**: username in case authentication is required
  - **smtp_password**: password in case authentication is required


- **batch_config**
  - **number_of_emails** (integer)\*: number of email messages to send
  - **min_wait** (integer)\*: minimum number of seconds to wait between consecutive messages, can be 0, must be smaller than min_wait.
  - **max_wait** (integer)\*: maximum number of seconds to wait to between consecutive messages, can 0, must be larger than max_wait. If max_wait if not 0, the script will randomize an integer number between min_wait and max_wait to be the number of seconds to wait between consecutive emails 
  - **randomize_senders** (boolean)\*: if true, message->from will be overriden by the list of senders in ```batch_config->senders_override``` (next). The script will randomize a sender for each email message sent out.
  - **senders_override** (array of strings): list of senders to randomize if ```batch_config->randomize_senders``` is set to ```true```.
  - **randomize_attachements** (boolean)\*: if true, ```message-->attachement``` is ignored, and a random file will be selected for each message.
