#/bin/bash

# Set mode, port
MODE=server
PORT=7777
CLIENT_ID="7mjrb3lKMrT9UIGQwmSB"
CLIENT_SECRET="5O9ezGkzdy"

python app.py --mode $MODE --port $PORT --client_id $CLIENT_ID --client_secret $CLIENT_SECRET

