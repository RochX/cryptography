
import React from 'react';

import { usePapaParse } from 'react-papaparse';

import './CSVParser.css'

export default function ReadRemoteFile() {
  const { readRemoteFile } = usePapaParse();

  const [data, setData] = React.useState([]);

  const handleReadRemoteFile = () => {
    readRemoteFile("http://localhost:4500/csv", {
      complete: (results) => {

        console.log('---------------------------');    
        console.log("Candidate A: " + evenElements(results.data[0]))
        console.log("Candidate B: " + evenElements(results.data[1]))
        console.log("Candidate C: " + evenElements(results.data[2]))
        console.log("Candidate D: " + evenElements(results.data[3]))
        console.log('---------------------------');
        var A = arrayToString(evenElements(results.data[0]))
        var B = arrayToString(evenElements(results.data[1]))
        var C = arrayToString(evenElements(results.data[2]))
        var D = arrayToString(evenElements(results.data[3]))
        var arr = [A, B, C, D]
        setData(arr);
      },
    });
  };

  return (
    <div className='ListContainer'>
      <div className='List'><span>Candidate A:  </span>{data[0]} </div>
      <div className='List'><span>Candidate B:  </span>{data[1]}</div>
      <div className='List'><span>Candidate C:  </span>{data[2]}</div>
      <div className='List'><span>Candidate D:  </span> {data[3]}</div>
      <button onClick={() => handleReadRemoteFile()}>Get Current Results</button>
    </div>
  );
}

//function to return the even elements from array without the first element
function evenElements(arr) {
  arr = arr.filter((element, index) => index % 2 === 0); //filter out even elements
  arr.shift(); //remove the first element
  return arr
}

//function to convert array to string with commas
function arrayToString(arr) {
  var str = '';
  for (var i = 0; i < arr.length; i++) {
    str += arr[i] + ', ';
  }
  return str.substring(0, str.length - 2);
}