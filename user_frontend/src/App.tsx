import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="MainFlex">
        <div className="MainFlex-Left">
          <div className='Card' id='firstCard'>
            <p>secure voting system</p>
            <div id='firstCard-line'></div>
          </div>
          <div className='Card' id='fourthCard'>
            <h1>
              3. See Results
            </h1>


          </div>
        </div>
        <div className="MainFlex-Right">
          <div className='Card' id='secondCard'>
            <h1>
              1. Register
            </h1>
            <input type="text" placeholder='first name'></input>
            <input type="text" placeholder='last name'></input>
            <input type="password" placeholder='SSN'></input>
            <button>GET ID</button>
          </div>

          <div className='Card' id='thirdCard'>
            <h1>
              2. Vote
            </h1>
            <input type="text"  placeholder='your ID'></input>
          
            <div className='Card-Vote-MainFlex'>
              <div className='Card-Vote-MainFlex-Left'>
                <button>Option A</button>
                <button>Option B</button>
              </div>
              <div className='Card-Vote-MainFlex-Right'>
                <button>Option C</button>
                <button>Option D</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
    </div>
  );
}

export default App;
