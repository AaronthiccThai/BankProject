import React, { useEffect, useState } from "react";
import { data, Form } from "react-router-dom";

          
const Dashboard = () => {
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
  const handleFormSubmit = async(e) => {
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

  return (
      <div>
        <ul>
          <li>
            <a href="#">Home</a>
            <a href="#">Transactions</a>
            <button onClick={handleToggleForm}>Add Card</button>
            </li>

        </ul>
        {showAllCards && (
          <div class="table-container"> 
            <h2>Your cards</h2>
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
                  </tr>
                ))}
              </tbody>
          </div> 
        )}
        {showCardForm && (
          <form onSubmit={handleFormSubmit} class="card-form"> 
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
      </div>

    );
  };
    
export default Dashboard;