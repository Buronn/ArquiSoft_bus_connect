#!/bin/bash
sshpass -e ssh -tt -L *:5000:localhost:5000 -o StrictHostKeyChecking=no ${USER}@${SERVER} 'date; /bin/bash'