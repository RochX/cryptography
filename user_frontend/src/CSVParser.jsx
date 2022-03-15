
import React from 'react';

import { usePapaParse } from 'react-papaparse';

export default function ReadRemoteFile() {
  const { readRemoteFile } = usePapaParse();

  const handleReadRemoteFile = () => {
    readRemoteFile("http://localhost:4500/csv", {
      complete: (results) => {
        console.log('---------------------------');
        console.log('Results:', results);
        console.log('---------------------------');
      },
    });
  };

  return <button onClick={() => handleReadRemoteFile()}>Get Current Results</button>;
}