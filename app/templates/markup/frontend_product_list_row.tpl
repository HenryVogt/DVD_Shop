<tr>
    <td><button type="submit" name="add_to_basket" value="{product[prod_id]}" class="btn btn-primary btn-xs">+ zum Warenkorb</button></td>
    <td>{product[prod_id]}</td>
    <td><a href="{root_path}/produkte?categoryname={product[categoryname]}&amp;precise=true">{product[categoryname]}</a></td>
    <td>{product[title]}</td>
    <td><a href="{root_path}/produkte?actor={product[actor]}&amp;precise=true">{product[actor]}</a></td>
    <td>{product[price]}</td>
</tr>