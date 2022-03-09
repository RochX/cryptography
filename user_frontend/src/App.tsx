import React, { useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  const [button1Selected, setButton1] = React.useState(false);
  const [button2Selected, setButton2] = React.useState(false);
  const [button3Selected, setButton3] = React.useState(false);
  const [button4Selected, setButton4] = React.useState(false);
  const [voted, setVoted] = React.useState(false);

  var firstName = "";
  var lastName = "";
  var SSN = "";
  var id = "";
  var selectedOption = "";

  const [card1Message, setCard1Message] = React.useState("");
  const [card2Message, setCard2Message] = React.useState("");

  function handleRegisterButton(){
    alert(firstName + " " +lastName + " " + SSN)
  }

  function selectButton(number: number){
    if ( id !== "" ){
      switch(number){
        case 1:
          setButton1(!button1Selected);
          setButton2(false);
          setButton3(false);
          setButton4(false);
          selectedOption = "A";
          setCard2Message("Successfully voted for option A");
          setVoted(true);
          break;
        case 2:
          setButton2(!button2Selected);
          setButton1(false);
          setButton3(false);
          setButton4(false);
          selectedOption = "B";
          setCard2Message("Successfully voted for option B");
          setVoted(true);
          break;
        case 3:
          setButton3(!button3Selected);
          setButton1(false);
          setButton2(false);
          setButton4(false);
          selectedOption = "C";
          setCard2Message("Successfully voted for option C");
          setVoted(true);
          break;
        case 4:
          setButton4(!button4Selected);
          setButton1(false);
          setButton2(false);
          setButton3(false);
          selectedOption = "D";
          setCard2Message("Successfully voted for option D");
          setVoted(true);
          break;
      }
    } else {
      setCard2Message("Please provide your ID first");
    }
  }

  return (
    <div className="App">
      <div className="MainFlex">
        <div className="MainFlex-Left">
          <div className='Card' id='firstCard'>
            <h1>secure voting system</h1>
            <div id='firstCard-line'></div>
          </div>
          <div className='Card' id='fourthCard'>
            <h2>
              3. See Results
            </h2>
          </div>
        </div>
        <div className="MainFlex-Right">
          <div className='Card' id='secondCard'>
            <h2>
              1. Register
            </h2>
            <input type="text" placeholder='first name' onChange={(e) => firstName = e.target.value}></input>
            <input type="text" placeholder='last name' onChange={(e) => lastName = e.target.value}></input>
            <input type="password" placeholder='SSN' onChange={(e) => SSN = e.target.value}></input>
            <button onClick={handleRegisterButton}>GET ID</button>
          </div>

          <div className='Card' id='thirdCard'>
            <h2>
              2. Vote
            </h2>
            <input disabled = {voted} type="text"  placeholder='your ID' onChange={(e) => id = e.target.value}></input>
            <p className={voted ? "Success" : "Error"}>{card2Message}</p>
            <div className='Card-Vote-MainFlex'>
              <div className='Card-Vote-MainFlex-Left'>
                <button 
                  disabled = {voted}
                  onClick={() => selectButton(1)}
                  className={button1Selected ? "Card-Vote-MainFlex-SelectedButton" : "" }
                >
                  Option A
                </button>
                <button 
                  disabled = {voted}
                  onClick={() => selectButton(2)}
                  className={button2Selected ? "Card-Vote-MainFlex-SelectedButton" : "" }>
                  Option B
                </button>
              </div>
              <div className='Card-Vote-MainFlex-Right'>
                <button 
                  disabled = {voted}
                  onClick={() => selectButton(3)}
                  className={button3Selected ? "Card-Vote-MainFlex-SelectedButton" : "" }
                >
                  Option C
                </button>
                <button 
                  disabled = {voted}
                  onClick={() => selectButton(4)}
                  className={button4Selected ? "Card-Vote-MainFlex-SelectedButton" : "" }
                >
                  Option D
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
    </div>
  );
}

export default App;
