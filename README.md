Create project in console.cloud.google.com
Enable google assistant in your project
Retrieve and store `client_secret.json`

```bash
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x ./get_tokens.sh
./get_tokens.sh
python assistant.py
```