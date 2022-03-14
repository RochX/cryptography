# NEEDS TO BE RUN WITH SUDO ACCESS (to install PM2)
# run init python
 pip3 install cryptography
 echo 'Node Version:'
 node -v
 echo '----------------------------------------'
 echo 'Installing/checking all dependencies...'
 echo '----------------------------------------'
 echo 'PM2 (a process manager to run everything in background)'
 echo 'https://pm2.keymetrics.io/'
 npm install pm2 -g
 echo '----------------------------------------'
 echo 'Stopping all running processes... (if any)'
 pm2 stop all
 pm2 delete all
 echo '----------------------------------------'
 echo 'CLA_BACKEND:'
 cd cla_backend
 npm install
 pm2 start node cla.js
echo '----------------------------------------'
 echo 'USER_BACKEND:'
 cd ../ctf_backend
 npm install
 pm2 start node ctf.js
echo '----------------------------------------'
 echo 'CTF_BACKEND:'
 cd ../user_backend
 npm install
 pm2 start node user.js
 echo 'USER_FRONTEND:'
 echo '----------------------------------------'
 cd ../user_frontend
 pm2 start npm --name "frontend" -- run start
 echo '----------------------------------------'
 echo 'CLA_backend: http://localhost:4000/'
 echo 'CTF_backend: http://localhost:5000/'
 echo 'User_backend: http://localhost:3500/'
 echo 'User_frontend: http://localhost:3000/'
 echo '----------------------------------------'
 echo 'To stop all servers type: "pm2 stop all"'