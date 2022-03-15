import React, { useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import Parser from './CSVParser';

function App() {

  const [button1Selected, setButton1] = React.useState(false);
  const [button2Selected, setButton2] = React.useState(false);
  const [button3Selected, setButton3] = React.useState(false);
  const [button4Selected, setButton4] = React.useState(false);
  const [voted, setVoted] = React.useState(false);
  const [registered, setRegistered] = React.useState(false);

  var firstName = "";
   var lastName = "";
   var SSN = "";
   var [id, setId] = React.useState<number>();
   var nickname = "";
   var selectedOption = "";

   const [card1Message, setCard1Message] = React.useState("");
   const [card2Message, setCard2Message] = React.useState("");

   async function handleRegisterButton(){
     if (firstName !== "" && lastName !== "" && SSN !== ""){
      fetch('http://localhost:4000/register/?firstName=' + firstName + '&lastName=' + lastName + '&SSN=' + SSN)
        .then(response => response.json())
        .then((response) => {
            if (response.output == "Invalid Personal Info.\n"){
              setCard1Message("Invalid personal infromation");
              setRegistered(false);
            } else {
              setCard1Message(response.output);
              setRegistered(true);
            }
         })
     } 
   }

   function handleVoteButton(number: number) {
    switch(number){
      case 1:
        selectedOption = "A";
        break;
      case 2:
        selectedOption = "B";
        break;
      case 3:
        selectedOption = "C";
        break;
      case 4:
        selectedOption = "D";
        break;
    }
    if (id || 0 > 0 && nickname !== ""  && selectedOption !== ""){
      fetch('http://localhost:4500/vote/?id=' + id + '&nickname=' + nickname + '&selectedOption=' + selectedOption)
        .then(response => response.json())
        .then((response) => {
          if (response.output == "You did not register in time.\n\n"){
            setCard2Message("The provide ID is not valid");
          }
          else if(response.output == "You already voted.\n"){
            setCard2Message("You have already voted");
          } else {
            switch(number){
              case 1:
                setButton1(!button1Selected);
                setButton2(false);
                setButton3(false);
                setButton4(false);
                setCard2Message("Successfully voted for option A");
                setVoted(true);
                break;
              case 2:
                setButton2(!button2Selected);
                setButton1(false);
                setButton3(false);
                setButton4(false);
                setCard2Message("Successfully voted for option B");
                setVoted(true);
                break;
              case 3:
                setButton3(!button3Selected);
                setButton1(false);
                setButton2(false);
                setButton4(false);
                setCard2Message("Successfully voted for option C");
                setVoted(true);
                break;
              case 4:
                setButton4(!button4Selected);
                setButton1(false);
                setButton2(false);
                setButton3(false);
                setCard2Message("Successfully voted for option D");
                setVoted(true);
                break;
              }
          }
         })
     } 
   }

   function selectButton(number: number){
     if ( id || 0 > 0 && nickname !== ""){
      handleVoteButton(number)
     } else {
       if (id || 0 > 0 && nickname === ""){
         setCard2Message("Please provide your ID and a nickname first");
       }
       else if (id || 0  > 0 ){
         setCard2Message("Please provide your ID first");
       } else if (nickname === ""){
         setCard2Message("Please provide an anonymous nickname first");
       }
     }
   }

  function keepNumbersOnly(e: React.ChangeEvent<HTMLInputElement>){
    const value = e.target.value.replace(/\D/g, "");
    setId(Number(value));
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
            {Parser()}
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
            <p className={registered ? "Success" : "Error"}>{card1Message}</p>
            <button 
              onClick={handleRegisterButton}
              disabled={registered}
              className={registered === false ? "" : "Card-MessageButton"}
            >
              GET ID
            </button>
          </div>
          <div className='Card' id='thirdCard'>
            <h2>
               2. Vote
             </h2>
             <input disabled = {voted} type="text"  placeholder='your ID' onChange={(e) => keepNumbersOnly(e)} value={id !== 0 ? id : ""}></input>
             <input disabled = {voted} type="text"  placeholder='anonymous nickname' onChange={(e) => nickname = e.target.value}></input>
             <p className={voted ? "Success" : "Error"}>{card2Message}</p>
             <div className='Card-Vote-MainFlex'>
               <div className='Card-Vote-MainFlex-Left'>
                <button 
                  disabled = {voted}
                  onClick={() => selectButton(1) }
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