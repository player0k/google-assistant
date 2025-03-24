* Create project in console.cloud.google.com
* Enable google assistant api in your project
* Setup Oauth 2.0 for your project in console.cloud.google.com for desktop application
* Add test users
* Retrieve and store `client_secret.json`

```bash
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
./get_tokens.sh
python assistant.py
```