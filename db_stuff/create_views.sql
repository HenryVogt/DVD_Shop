CREATE VIEW products_view AS
	SELECT 
		p.prod_id, 
		c.categoryname,
		p.title,
		p.actor,
		p.price,
		p.special,
		p.common_prod_id,
		i.quan_in_stock
	FROM products p
		INNER JOIN categories c ON p.category = c.category
		LEFT JOIN inventory i ON p.prod_id = i.prod_id;
		
CREATE VIEW products_available_view AS
	SELECT 
		*
	FROM products_view
	WHERE
	    quan_in_stock > 0;

CREATE VIEW orders_view AS
	SELECT 
		orders.orderid, 
		orders.orderdate, 
		orders.customerid, 
		customers.firstname AS customer_firstname, 
		customers.lastname AS customer_lastname,
		orders.netamount,
		orders.tax,
		orders.totalamount
	FROM orders
	NATURAL JOIN customers;

CREATE VIEW orderlines_view AS
	SELECT orderlines.orderlineid, orderlines.orderid, orderlines.quantity, orderlines.prod_id, products.title
	FROM orderlines
	LEFT JOIN products ON orderlines.prod_id = products.prod_id;
