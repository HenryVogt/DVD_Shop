		<tr>
			<td>Bestell-Nr.</td>
	        <td>{order[orderid]}</a></td>
		</tr>
		<tr>
			<td>Datum</td>
	        <td>{order[orderdate]}</td>
		</tr>
		<tr>
			<td>Kunde</td>
	        <td><a href="{root_path}/kunden/{order[customerid]}">{order[customer_firstname]} {order[customer_lastname]}</a></td>
		</tr>
		<tr>
			<td>Nettobetrag</td>
	        <td>{order[netamount]} EUR</td>
		</tr>
		<tr>
			<td>MwSt.</td>
	        <td>{order[tax]} EUR</td>
		</tr>
		<tr>
			<td>Gesamtbetrag</td>
	        <td>{order[totalamount]} EUR</td>
		</tr>
