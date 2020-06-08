//templates for menu.js

export const add_to_cart_form_template = Handlebars.compile(`
<form class="add-to-cart-form">
<input type="hidden" name="item_id" value={{ item_id }}>
{{#each addons}}
	<label>{{ this.name }}{{ formatAddonPrice this.price }}</label>
	<input type="checkbox" name="addon" value="{{ this.id }}">
	<br>
{{/each}}
<input type=submit value="Add to Cart">
</form>`);

export const cart_template = Handlebars.compile(`
	{{#each items}}
		<b>{{this.size}} {{this.category}}</b>
		</br>
		{{this.name}}
		</br>
		\${{this.base_price}}
		</br>
		{{#each this.addons}}
			+{{this.name}}
			{{ formatAddonPrice this.price }}
			<br/>
		{{/each}}
		<br/>
	{{/each}}
	<div id="total-price"><h3>Total: \${{total_price}}</h3></div>`);

//templates for place_order.js

export const cart_table_template = Handlebars.compile(`
<table id="order-items-table">
	<tr>
		<td>#</td>
		<td>Item</td>
		<td>
			Base Price
			<i 
				class="fa fa-info-circle" 
				data-tippy-content="Price without addons.">
			</i>
		</td>
		<td>
		Total Price
		<i 
			class="fa fa-info-circle" 
			data-tippy-content="Price with addons.">
		</i>
		</td>
		<td></td>
	</tr>
{{#each items}}
	<tr>
		<td>{{counter @index}}</td>
		<td class="item-name-col-td">{{this.size}} {{this.category}} {{this.name}}</td>
		<td>\${{this.base_price}}</td>
		<td>\${{this.total_price}}</td>
		<td>
			<i class="fa fa-trash-o rm-from-cart-btn" data-item="{{ this.id }}"></i>
		</td>
	</tr>

	{{#if this.addons}}
	<tr>
		<td></td>
		<td colspan=4 class="item-name-col-td">
			<ul>
			{{#each this.addons}}
			<li>{{this.name}} {{ formatAddonPrice this.price }}</li>
			</ou>
		{{/each}}
	</td>
	</tr>
	{{/if}}

{{/each}}
</table>
`);

//helpers

//1-indexed counter. Usage: {{counter @index}}
Handlebars.registerHelper("counter", index => index + 1);

//returns empty string if price==0.00 otherwise adds $ symbol in the front
Handlebars.registerHelper('formatAddonPrice', price => price == 0.00 ? '' : `(+\$${price})`);