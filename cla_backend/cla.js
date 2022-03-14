const express = require('express');
const cors = require('cors')
const {spawn} = require('child_process');
const app = express();
app.use(cors());

const port = 4000

app.get('/', (req, res) => {
 
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['../python/testCLA.py']);
    // collect data from script
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
    });

    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    res.send({output: "hello"})
    });
})

app.get('/register', (req, res) => {

    var firstName = req.query.firstName
    var lastName = req.query.lastName
    var SSN = req.query.SSN

    console.log(firstName)
 
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['../python/UsertoCLA.py', firstName, lastName, SSN],);
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

app.listen(port, () => console.log(`CLA: Example app listening on port ${port}!`))