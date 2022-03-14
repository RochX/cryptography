const express = require('express');
const cors = require('cors')
const {spawn} = require('child_process');
const app = express();
app.use(cors());

const port = 4500

app.get('/', (req, res) => {
 
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['../python/testCTF.py']);
    // collect data from script
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
    });

    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    res.send({output: dataToSend})
    });
})

app.get('/vote', (req, res) => {

    var id = req.query.id
    var nickname = req.query.nickname
    var selectedOption = req.query.selectedOption

    console.log(id, nickname, selectedOption)
 
    var dataToSend;

    process.chdir("../python")
    // spawn new child process to call the python script
    const python = spawn('python3', ['UsertoCTF.py', selectedOption, id, nickname]);
    // collect data from script
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
    });

    python.on('exit', (code, signal) => {
        if (code) {
            console.error('Child exited with code', code)
        } else if (signal) {
            console.error('Child was killed with signal', signal);
        } else {
            console.log('Child exited okay');
        }
    });

    python.stderr.on('data', (data) => {
        console.log(data.toString());
    });

    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
        res.send({output: dataToSend})
    });
})

app.listen(port, () => console.log(`CTF: Example app listening on port ${port}!`))