import React, { useEffect, useState} from "react";

const Transaction = () => {

	const [transactions, setTransactions] = useState([]);
	const fetchTransaction = async() => {
		const url = "http://localhost:5000/transaction/get_transactions"	
		try {
			const response = await fetch(url, {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
					Authorization: `Bearer ${localStorage.getItem("token")}`, 
				}
			})
			const data = await response.json()
			if (response.ok) {
				setTransactions(data.transactions)
			} else {
				alert(data.message)
			}
		} catch (error) {
			console.log(error);
		}
	}
	useEffect(() => {
		fetchTransaction()
	}, [])
	return (
		<div> 
			<h2> Your transactions</h2>
			<table> 
				<thead> 
					<tr> 
						<th> Transaction ID </th> 
						<th> Source CardID </th>
						<th> Target CardID </th>
						<th> Transaction Type </th>
						<th> Amount </th>
						<th> Time </th>																								
					</tr>
				</thead>
				<tbody> 
					{transactions.map((transaction, index) => (
						<tr key={index}>
							<td> {transaction.transaction} </td> 
							<td> {transaction.source_card} </td> 
							<td> {transaction.target_card} </td> 
							<td> {transaction.transaction_type} </td> 
							<td> {transaction.amount} </td> 
							<td> {transaction.time} </td> 
						</tr>
					))}

				</tbody>

			</table>
		</div>
	)

}
export default Transaction;