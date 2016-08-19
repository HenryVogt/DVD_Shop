<tr>
    <td><a href="{root_path}/bestellungen/{order[orderid]}" class="btn btn-primary btn-sm">Details</a></td>
    <td>{order[orderid]}</td>
    <td>{order[orderdate]:%d. %B %Y}</td>
    <td><a href="{root_path}/kunden/{order[customerid]}">{order[customer_firstname]} {order[customer_lastname]}</a></td>
    <td>{order[netamount]} €</td>
    <td>{order[tax]} €</td>
    <td>{order[totalamount]} €</td>
</tr>