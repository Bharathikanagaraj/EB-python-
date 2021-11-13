import json
import csv
# import all json files in list
json_files = [open("C://Users/Bharathi K/Desktop/sample_docs/maojson_1.json"),open("C://Users/Bharathi K/Desktop/sample_docs/maojson_2.json"),open("C://Users/Bharathi K/Desktop/sample_docs/maojson_5.json"),open("C://Users/Bharathi K/Desktop/sample_docs/auth_mismatch_with_tax.json")]
# set fields
fields = ["Placed On","OrderId","OrderStatus","Price_Without_Tax","UP+TAX+SHIPPING","AmtPaid","Difference","Paid_CC_PAYPAL","GC_REWARDCARD Amt","paymentCount"]
# set empty rows
rows =[]

for file in json_files:
    # open json and load data     
    data = json.load(file)
    file.close()
    # empty set
    values = {}

    values[fields[0]] = data["CapturedDate"]
    values[fields[1]] = data["OrderId"]
    # OrderStatus
    order_status = "null"
    if data["IsConfirmed"] and not data["IsOnHold"]:
        order_status = 'Placed Successfully'
    elif not data["IsConfirmed"] and data["IsOnHold"]:
        order_status = 'On-Hold'
    values[fields[2]] = order_status
    # Unit_price / Price_Without_Tax
    unit_price = 0
    for price in data["OrderLine"]:
        unit_price = round((float(unit_price) + float(price["UnitPrice"])), 2)
    values[fields[3]] = unit_price
    # AmtPaid
    paid_amount = data["Payment"][0]["PaymentMethod"][0]["Amount"]
    values[fields[5]] = paid_amount
    # UP+TAX+SHIPPING
    payment_method = data["Extended"]["PrimaryPaymentMethod"]
    gc_rewards_amt = 0
    if payment_method == 'Gift Card':
        gc_rewards_amt = paid_amount
    else:
        order_details = data["OrderLine"]
        tax = 0
        for order_line_tax in order_details:
            unit_tax = order_line_tax["OrderLineTaxDetail"]
            for tax_amount in unit_tax:
                tax = round((tax + tax_amount["TaxAmount"]), 2)

        orders = data["OrderTaxDetail"]
        order_tax_details = 0
        for order in orders:
            order_tax_details = order_tax_details + order["TaxAmount"]

        tax = tax + order_tax_details
        shipping_amounts = data["OrderChargeDetail"]
        final_shipping_amount = 0

        for ChargeTotal in shipping_amounts:
            final_shipping_amount = final_shipping_amount + round(ChargeTotal.get("ChargeTotal"), 2)
        tax_shipping = round((tax + final_shipping_amount), 2)
    unit_price = 0
    for price in data["OrderLine"]:
        unit_price = round((float(unit_price) + float(price["UnitPrice"])), 2)
    tax_shipping_unit = round((round(tax_shipping, 2) + round(unit_price, 2)), 2)
    values[fields[4]] = tax_shipping_unit
    # difference
    if paid_amount == tax_shipping_unit:
        difference = 0
    else:
        difference = round((paid_amount - tax_shipping_unit), 2)
    values[fields[6]] = difference
    # GC_REWARDCARD Amt
    values[fields[8]] = gc_rewards_amt
    # payment_count
    payment_count = 0
    credit_card = 0
    paypal =0
    pay = data["Payment"]
    for get_pay in pay:
        for pay_type in get_pay["PaymentMethod"]:
            if "Credit Card" in pay_type["PaymentType"].values():
                payment_count += 1
                credit_card += 1
            elif "PayPal" in pay_type["PaymentType"].values():
                payment_count += 1
                paypal += 1
            elif "Gift Card" in pay_type["PaymentType"].values():
                payment_count += 1
            elif "Loyalty Certificate" in pay_type["PaymentType"].values():
                payment_count += 1
    values[fields[9]] = payment_count
    # Paid_CC_PAYPAL
    values[fields[7]] = paypal
    #  assign the values into a single row
    rows.append(values)
# o/p verfication
print(rows)
# writing into csv file
with open("C://Users/Bharathi K/Desktop/sample_docs/op.csv", 'w', newline='') as csvfile:
    # creating a csv dict writer object 
    writer = csv.DictWriter(csvfile, fieldnames = fields)
    # writing headers (field names) 
    writer.writeheader()
    # writing data rows
    writer.writerows(rows)
