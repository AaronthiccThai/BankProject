import React, { useEffect, useState } from "react";
import { data, Form } from "react-router-dom";
import Header from "./Header.js";
          
const Dashboard = () => {
  ////////////////////////////////////////////////////////////////////////////////////
  // For add card form
  const [showCardForm, setCardShowForm] = useState(false);
  const [cardDetails, setCardDetails] = useState({
    cardNumber: "",
    expDate: "",
    cvv: "",
  });
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCardDetails({ ...cardDetails, [name]: value });
  };

  const handleToggleForm = () => {
    setCardShowForm(!showCardForm);
  };
  const CreateCardFormSubmit = async(e) => {
    e.preventDefault();
    const url = "http://localhost:5000/bank/addcard";
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`, 
        },
        body: JSON.stringify(cardDetails)
      });
      const data = await response.json();

      if (response.ok) {
        alert(data.message)
        setCardDetails({ cardNumber: "", expDate: "", cvv: "" });
        setCardShowForm(false); 
        fetchCards()          
      } else {
        alert(data.message)
      }
    } catch (error) {
      console.error("Error:", error);
    }
 
  }
  ////////////////////////////////////////////////////////////////////////////////////
  // For remove a card
  const [showDeleteCardForm, setDeleteForm] = useState(false);
  const [deleteCardDetails, setDeleteCardDetails] = useState({
    cardNumber: "",
  });
  const [isConfirmed, setIsConfirmed] = useState(false); // Checkbox

  const toggleDeleteForm = () => {
    setDeleteForm(!showDeleteCardForm)
  }

  const handleDeleteInputChange = (e) => {
    const { name, value } = e.target;
    setDeleteCardDetails({ ...deleteCardDetails, [name]: value });
  };

  const handleCheckboxChange = (e) => {
    setIsConfirmed(e.target.checked);
  };

  const deleteCardFormSubmit = async(e) => {
    e.preventDefault()
    const url = "http://localhost:5000/bank/removecard"
    try {
      const response = await fetch(url, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,           
        },
        body: JSON.stringify(deleteCardDetails),
      });
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        setDeleteCardDetails({ cardNumber: ""});
        setDeleteForm(false);
        fetchCards();
      } else {
        alert(data.message)
      }
    } catch (error) {
      console.log(error);
    }
  }

  ////////////////////////////////////////////////////////////////////////////////////
  // For displaying all the users cards - acc number and bal
  const [showAllCards, setAllCards] = useState(true);
  const [cards, setCards] = useState([])

  const fetchCards = async () => {
    const url = "http://localhost:5000/bank/getcard";
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      const data = await response.json();

      if (response.ok) {
        setCards(data.cards);
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error("Error fetching cards:", error);
    }
  };

  useEffect(() => {
    fetchCards();
  }, []);

  ////////////////////////////////////////////////////////////////////////////////////
  // For displaying all actions for the bank card - withdraw, deposit, transfer
  const [selectedCard, setSelectedCard] = useState(null);
  const [showCardActions, setShowCardActions] = useState(false);
  const [selectedAction, setSelectedAction] = useState('');

  const handleShowActions = (card) => {
    setSelectedCard(card);
    setShowCardActions(!showCardActions);
  };
  const handleActionSubmit = async(e, targetCardID) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const action = formData.get("action");
    const amount = formData.get("amount");
    const url = `http://localhost:5000/transaction/${action}`;
    const payload = { targetCardID, amount };

    if (action === "transfer") {
      const transferCard = formData.get("transferCard");
      payload.transferCard = transferCard;
    }
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,          
        },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (response.ok) {
        fetchCards()
        alert(data.message)
        setShowCardActions(false);
      } else {
        alert(data.message);
        console.log(data.message);
      }
    } catch(error) {
      console.error("Error: ", error)
    }
  };

  ////////////////////////////////////////////////////////////////////////////////////
  return (
      <div>
        <Header 
          onToggleAddCardForm={handleToggleForm}
          onToggleRemoveCardForm={toggleDeleteForm}
        /> 
        {showAllCards && (
          <div class="table-container"> 
            <h2>Your cards</h2>
              <table> 
                <thead>
                  <tr>
                    <th> Card number </th>
                    <th> Balance </th>
                  </tr>
                </thead>
                <tbody>
                  {cards.map((card, index) => (
                    <tr key={index}>
                      <td>{card.card_id}</td>
                      <td>{card.balance}</td>
                      <td>
                        <button onClick={() => handleShowActions(card)}>Actions</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
          </div> 
        )}
        {showCardActions && selectedCard && (
          <div className="actions-container">
            <h2>Actions for Card: {selectedCard.card_id}</h2>
            <form onSubmit={(e) => handleActionSubmit(e, selectedCard.card_id)}>
              <label>
                Action:
                <select name="action" onChange={(e) => setSelectedAction(e.target.value)} required>
                  <option value="withdraw">Withdraw</option>
                  <option value="deposit">Deposit</option>
                  <option value="transfer">Transfer</option>
                </select>
              </label>
              <label>
                Amount:
                <input type="text" name="amount" pattern="\d+(\.\d{1,2})?" title="Please enter a valid decimal amount (e.g., 123.45)" required />
              </label>
              {selectedAction === "transfer" && (
                <label> Target Card Number
                  <input type="text" name="transferCard" title="Please enter target card number" required />  
                </label>
              )}
              <button type="submit">Submit</button>
            </form>
          </div>
        )}

        {showCardForm && (
          <form onSubmit={CreateCardFormSubmit} class="card-form"> 
            <h2>Add Card</h2>
            <div class="form-container">
              <label> Card Number:
                <input type="text" name="cardNumber" value={cardDetails.cardNumber} onChange={handleInputChange} required ></input>
              </label>
              <label> Exp Date:
                <input type="month" name="expDate" value={cardDetails.expDate} onChange={handleInputChange} required ></input>
              </label>
              <label> CVV:
                <input type="password" name="cvv" value={cardDetails.cvv} onChange={handleInputChange} maxLength="3" required ></input>
              </label>
              <button> Submit </button>
            </div>
          </form>
        )}    

        {showDeleteCardForm && (
          <form onSubmit={deleteCardFormSubmit} class="delete-form">
            <h2> Delete Card </h2>
            <div class="delete-container"> 
              <label> Card Number: 
                <input type="text" name="cardNumber" value={deleteCardDetails.cardNumber} onChange={handleDeleteInputChange} required></input>
              </label>
            </div>   
            <div class="checkbox-container">
              <label htmlFor="confirmCheckbox"> Confirm? </label>                  
              <input type="checkbox" checked={isConfirmed} onChange={handleCheckboxChange} required id="confirmCheckBox"></input>
            </div>  
            <button type="submit" disabled={!isConfirmed}> Submit </button>
          </form>
        )}        
      </div>

    );
  };
    
export default Dashboard;