const express = require('express');
const cors = require('cors')
const fetch = require('node-fetch');
const {spawn} = require('child_process');
const app = express();
app.use(cors());

const port = 3500

app.get('/', (req, res) => {
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['../python/test.py']);
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


//http://localhost:3500/register/?firstName=1&lastName=2&SSN=3
app.get('/register', (req, res) => {

    var firstName = req.query.firstName
    var lastName = req.query.lastName
    var SSN = req.query.SSN
 
    var dataToSend;
    console.log("register..")
    // spawn new child process to call the python script
    process.chdir("../python")
    // const python = spawn('python3', ['UsertoCLA.py', firstName, lastName, SSN]);
    // // collect data from script
    // python.stdout.on('data', function (data) {
    //     console.log('Pipe data from python script ...');
    //     dataToSend = data.toString();
    // });

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
    
    // localhost:4000/register/?firstName=1&lastName=2&SSN=3
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        fetch('http://localhost:4000/register/?firstName=' + firstName + '&lastName=' + lastName + '&SSN=' + SSN)
        .then(response => response.json())
            .then((response) => {
                console.log("FETCHING IS SUCCESSFUL" + response.output)
                //dataToSend = response.output.toString()
                res.send({output: dataToSend}) 
 
        });
    }); 
})

app.listen(port, () => console.log(`CTF: Example app listening on port ${port}!`))