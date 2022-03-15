# NEEDS TO BE RUN WITH SUDO ACCESS (to install PM2)
# The script will install several dependencies and 
# start 2 background servers, as well as the user interface
# web page. 
#
# ATTENTION! Tested only on macOS with the following Python and Node.js versions:
# - Python 3.10.0
# - Node.js v16.13.1
#
# To stop all the servers, run the following command: "pm2 stop all"

if [ "$EUID" -ne 0 ]
then echo "Please run with sudo permission."
exit
fi
echo 'Python Version:'
python3 --version
echo 'Node Version:'
node -v
echo '----------------------------------------'
echo 'Installing/checking all dependencies...'
echo '----------------------------------------'
echo 'PM2 (a process manager to run everything in background)'
echo 'https://pm2.keymetrics.io/'
npm install pm2 -g
echo '----------------------------------------'
echo 'cryptography (python package for the encryption)'
echo 'https://pypi.org/project/cryptography/'
pip3 install cryptography
echo '----------------------------------------'
echo 'INITIALIZING:'
cd python
python3 init_orgs.py
echo '----------------------------------------'
echo 'Stopping all running processes... (if any)'
pm2 stop all
pm2 delete all
echo '----------------------------------------'
echo 'CLA_BACKEND:'
cd ../cla_backend
npm install
pm2 start node cla.js
echo '----------------------------------------'
echo 'CTF_BACKEND:'
cd ../ctf_backend
npm install
pm2 start node ctf.js
echo '----------------------------------------'
echo 'USER_FRONTEND:'
cd ../user_frontend
npm install
pm2 start npm --name "frontend" -- run start
echo '----------------------------------------'
echo 'CLA_backend: http://localhost:4000/'
echo 'CTF_backend: http://localhost:4500/'
echo 'User_frontend: http://localhost:3000/'
echo '----------------------------------------'
echo 'To stop all servers type: "pm2 stop all"'