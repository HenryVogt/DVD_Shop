<form method="post" class="form-horizontal col-md-6">
	<div class="form-group">
		<label for="firstname">Vorname</label>
		<input type="text" id="firstname" name="firstname" class="form-control" value="{customer[firstname]}" />
	</div>

	<div class="form-group">
		<label for="lastname">Nachname</label> 
		<input type="text" id="lastname" name="lastname" class="form-control" value="{customer[lastname]}"/>
	</div>

	<div class="form-group">
		<label for="username">Username</label>
		<input type="text" id="username" name="username" class="form-control" value="{customer[username]}"/>
	</div>

	<div class="form-group">
		<label for="password">Password</label>
		<input type="text" id="password" name="password" class="form-control" value="{customer[password]}"/>
	</div>

	<div class="form-group">
		<label for="address1">Adresse 1</label>
		<input type="text" id="address1" name="address1" class="form-control" value="{customer[address1]}"/>
	</div>

	<div class="form-group">
		<label for="address2">Adresse 2</label>
		<input type="text" id="address2" name="address2" class="form-control" value="{customer[address2]}"/>
	</div>

	<div class="form-group">
		<label for="city">Stadt</label> 
		<input type="text" id="city" name="city" class="form-control" value="{customer[city]}"/>
	</div>

    <div class="form-group">
        <label for="state">Bundesstaat</label>
        <input type="text" id="state" name="state" class="form-control" value="{customer[state]}" />
    </div>

    <div class="form-group">
        <label for="zip">PLZ</label>
        <input type="text" id="zip" name="zip" class="form-control" value="{customer[zip]}" />
    </div>

	<div class="form-group">
		<label for="country">Land</label> 
		<input type="text" id="country" name="country" class="form-control" value="{customer[country]}"/>
	</div>

	<div class="form-group">
		<label for="region">Region</label>
		<input type="text" id="region" name="region" class="form-control" value="{customer[region]}"/>
	</div>

	<div class="form-group">
		<label for="age">Alter</label>
		<input type="text" id="age" name="age" class="form-control" value="{customer[age]}"/>
	</div>

    <div class="form-group">
		<label for="income">Einkommen</label>
		<input type="text" id="income" name="income" class="form-control" value="{customer[income]}"/>
	</div>

    <div class="form-group">
		<label for="gender">Geschlecht</label>
		<input type="text" id="gender" name="gender" class="form-control" value="{customer[gender]}"/>
	</div>

	<div class="form-group">
		<label for="email">E-Mail</label> 
		<input type="text" id="email" name="email" class="form-control" value="{customer[email]}"/>
	</div>

	<div class="form-group">
		<label for="phone">Telefon</label> 
		<input type="text" id="phone" name="phone" class="form-control" value="{customer[phone]}"/>
	</div>

	<div class="form-group">
		<label for="creditcarttype">Kreditkarten-Typ</label> 
		<input type="text" id="creditcardtype" name="creditcardtype" class="form-control" value="{customer[creditcardtype]}"/>
	</div>

	<div class="form-group">
		<label for="creditcart">Kreditkarte</label> 
		<input type="text" id="creditcard" name="creditcard" class="form-control" value="{customer[creditcard]}"/>
	</div>

	<div class="form-group">
		<label for="creditcartexpiration">Kreditkarte Ablaufdatum</label> 
		<input type="text" id="creditcardexpiration" name="creditcardexpiration" class="form-control" value="{customer[creditcardexpiration]}"/>
	</div>
	 
	<div class="form-group">
		<button type="reset" class="btn btn-cancel">Eingaben zurücksetzen</button> 
		<button type="submit" class="btn btn-primary">Eingaben absenden</button> 
	</div>
</form>