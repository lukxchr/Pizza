from .models import MenuItem, MenuItemAddon, OrderItem, OrderItemAddon
from collections import OrderedDict

#given cart representation stored inside session returns JSON serializable object 
def serialize_cart(pending_order):
	serialized = {'items' : []}
	total_price = 0
	for item in pending_order:
		menu_item = MenuItem.objects.get(pk=item['item_id'])
		addons = [MenuItemAddon.objects.get(pk=id_) for id_ in item['addon_ids']]
		total_price += menu_item.price + sum(addon.price for addon in addons)
		serialized_item =  {
			'id' : item['id'],
			'name' : menu_item.name,
			'category' : menu_item.category.name,
			'size' : menu_item.size.name if menu_item.size else None,
			'base_price' : menu_item.price,
			'total_price' : menu_item.price + sum(addon.price for addon in addons),
			'addons' : [{'name': addon.name, 'price': addon.price} for addon in addons],
		}	
		serialized['items'].append(serialized_item)
	serialized['total_price'] = total_price
	return serialized

#adds all items from cart(pending_order stored in session)
#to db and links them with order instance
def save_cart(pending_order, order):
	for item in pending_order:
		menu_item = MenuItem.objects.get(pk=item['item_id'])
		order_item = OrderItem(menu_item=menu_item, order=order)
		order_item.save()
		for addon_id in item['addon_ids']:
			menu_item_addon = MenuItemAddon.objects.get(pk=addon_id)
			order_item_addon = OrderItemAddon(
				menu_item_addon=menu_item_addon, order_item=order_item)
			order_item_addon.save()

#given category returns data for menu template
#{'header': [], 'rows': [[],]}
def build_menu_table(category):
	menu_items = MenuItem.objects.filter(category=category) 
	#build list with distinct sizes/item names while keeping order 
	distinct_sizes = list(OrderedDict.fromkeys(menu_item.size for menu_item in menu_items))
	distinct_item_names = list(OrderedDict.fromkeys(menu_item.name for menu_item in menu_items))
	header = [None] + [size.name if size else '' for size in distinct_sizes]
	rows = []
	for name in distinct_item_names:
		row = [name]
		for size in distinct_sizes:
			item = menu_items.filter(name=name, size=size).first()
			row.append(item if item else None)
		rows.append(row)
	return {'header': header, 'rows': rows}
