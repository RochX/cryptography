
import React from 'react';

import { usePapaParse } from 'react-papaparse';

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
        var A = evenElements(results.data[0])
        var B = evenElements(results.data[1])
        var C = evenElements(results.data[2])
        var D = evenElements(results.data[3])
        var arr = [A, B, C, D]
        setData(arr);
      },
    });
  };

  return (
    <div>
      <div>Candidate A: {data[0]}</div>
      <div>Candidate B: {data[1]}</div>
      <div>Candidate C: {data[2]}</div>
      <div>Candidate D: {data[3]}</div>
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