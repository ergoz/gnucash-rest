import gnucash
from gnucash.gnucash_business import Entry

def addressToDict(address):
	if address is None:
		return None
	else:
		simple_address = {}
		simple_address['name'] = address.GetName();
		simple_address['line_1'] = address.GetAddr1();
		simple_address['line_2'] = address.GetAddr2();
		simple_address['line_3'] = address.GetAddr3();
		simple_address['line_4'] = address.GetAddr4();
		simple_address['phone'] = address.GetPhone();
		simple_address['fax'] = address.GetFax();
		simple_address['email'] = address.GetEmail();

		return simple_address

def vendorToDict(vendor):

	if vendor is None:
		return None
	else:
		'''

		vendor.GetTerms() needs to be converted from BillTerm
		vendor.GetTaxTable() errors - so is not tax_included

		'''

		simple_vendor = {}
		simple_vendor['name'] = vendor.GetName()
		simple_vendor['id'] =  vendor.GetID()
		simple_vendor['notes'] =  vendor.GetNotes()
		simple_vendor['active'] =  vendor.GetActive()
		#simple_vendor['discount'] =  vendor.GetDiscount().to_double()
		#simple_vendor['credit'] =  vendor.GetCredit().to_double()
		simple_vendor['currency'] =  vendor.GetCurrency().get_mnemonic()
		simple_vendor['tax_table_override'] =  vendor.GetTaxTableOverride()
		simple_vendor['address'] = addressToDict(vendor.GetAddr())
		#simple_vendor['terms'] =  vendor.GetTerms() # needs to be converted to string BillTerm
		simple_vendor['tax_included'] =  vendor.GetTaxIncluded()

		return simple_vendor

def customerToDict(customer):

	if customer is None:
		return None
	else:
		'''

		customer.GetTerms() needs to be converted from BillTerm
		customer.GetTaxTable() errors - so is not tax_included

		'''

		simple_customer = {}
		simple_customer['name'] = customer.GetName()
		simple_customer['id'] =  customer.GetID()
		simple_customer['notes'] =  customer.GetNotes()
		simple_customer['active'] =  customer.GetActive()
		simple_customer['discount'] =  customer.GetDiscount().to_double()
		simple_customer['credit'] =  customer.GetCredit().to_double()
		simple_customer['currency'] =  customer.GetCurrency().get_mnemonic()
		simple_customer['tax_table_override'] =  customer.GetTaxTableOverride()
		simple_customer['address'] = addressToDict(customer.GetAddr())
		simple_customer['shipping_address'] = addressToDict(customer.GetShipAddr())
		#simple_customer['terms'] =  customer.GetTerms() # needs to be converted to string BillTerm
		simple_customer['tax_included'] =  customer.GetTaxIncluded()

		return simple_customer

def transactionToDict(transaction):
	if transaction is None:
		return None
	else:
		simple_transaction = {}
		simple_transaction['num'] =  transaction.GetNum()
		simple_transaction['notes'] =  transaction.GetNotes()
		simple_transaction['is_closing_txn'] =  transaction.GetIsClosingTxn()
		#simple_transaction['get_split_list'] =  transaction.GetSplitList() # add in split list
		simple_transaction['count_splits'] =  transaction.CountSplits()
		simple_transaction['has_reconciled_splits'] =  transaction.HasReconciledSplits()
		simple_transaction['currency'] =  transaction.GetCurrency().get_mnemonic()
		simple_transaction['imbalance_value'] =  transaction.GetImbalanceValue().to_double()
		simple_transaction['is_balanced'] =  transaction.IsBalanced()
		simple_transaction['date'] =  transaction.GetDate()
		simple_transaction['date_posted'] =  transaction.RetDatePostedTS().strftime('%Y-%m-%d')
		simple_transaction['date_entered'] =  transaction.RetDateEnteredTS().strftime('%Y-%m-%d')
		simple_transaction['date_due'] =  transaction.RetDateDueTS().strftime('%Y-%m-%d')
		simple_transaction['void_status'] =  transaction.GetVoidStatus()
		simple_transaction['void_time'] =  transaction.GetVoidTime().strftime('%Y-%m-%d')

		return simple_transaction

def invoiceToDict(invoice):

	if invoice is None:
		return None
	else:
		simple_invoice = {}
		simple_invoice['id'] =  invoice.GetID()
		simple_invoice['type'] =  invoice.GetType()
		simple_invoice['date_opened'] =  invoice.GetDateOpened().strftime('%Y-%m-%d')
		simple_invoice['date_posted'] =  invoice.GetDatePosted().strftime('%Y-%m-%d')
		simple_invoice['date_due'] =  invoice.GetDateDue().strftime('%Y-%m-%d')
		simple_invoice['notes'] =  invoice.GetNotes()
		simple_invoice['active'] =  invoice.GetActive()
		simple_invoice['currency'] =  invoice.GetCurrency().get_mnemonic()
		simple_invoice['owner'] =  vendorToDict(invoice.GetOwner()) 
		simple_invoice['owner_type'] =  invoice.GetOwnerType() # owner type ?
		
		#simple_invoice['terms'] =  invoice.GetTerms() # needs to be converted to string BillTerm
		simple_invoice['billing_id'] =  invoice.GetBillingID()
		simple_invoice['to_charge_amount'] = invoice.GetToChargeAmount().to_double()
		#simple_invoice['bill_to'] =  invoice.GetBillTo()
		## This causes a segfault for us
		##simple_invoice['posted_txn'] =  transactionToDict(invoice.GetPostedTxn())
		#simple_invoice['posted_lot'] =  invoice.GetPostedLot()
		#simple_invoice['posted_account'] =  invoice.GetPostedAcc()
		simple_invoice['total'] = invoice.GetTotal().to_double()
		#simple_invoice['billto_type'] =  invoice.GetBillTo()
		#simple_invoice['billto_guid'] =  invoice.GetID()
		#simple_invoice['charge_amount'] =  invoice.GetChargeAmount()
		#simple_invoice['charge_amt_denom'] =  invoice.GetID()

		simple_invoice['total_subtotal'] = invoice.GetTotalSubtotal().to_double()
		#simple_invoice['total_of'] = invoice.GetTotalOf() # takes more args
		simple_invoice['total_tax'] = invoice.GetTotalTax().to_double()
		# COME BACK TO ENTRIES
		#

		#should this be a list rather than a dict?
		simple_invoice['entries'] = {}
		for n, entry in enumerate(invoice.GetEntries()): 
			if type(entry) != Entry:
				entry=Entry(instance=entry) 
			simple_invoice['entries'][n] = entryToDict(entry)
		#simple_invoice['entries'] = entryToDict(invoice.GetEntries())
		#
		#simple_invoice['prices'] = invoice.GetPrices() 
		#simple_invoice['price'] = invoice.GetPrice() # takes more args
		simple_invoice['posted'] = invoice.IsPosted()
		simple_invoice['paid'] = invoice.IsPaid()

		return simple_invoice

def entryToDict(entry):

	if entry is None:
		return None
	else:

		simple_entry = {}
		simple_entry['date'] =  entry.GetDate().strftime('%Y-%m-%d')
		simple_entry['date_entered'] =  entry.GetDateEntered().strftime('%Y-%m-%d')
		simple_entry['description'] =  entry.GetDescription()
		simple_entry['action'] =  entry.GetAction()
		simple_entry['notes'] =  entry.GetNotes()
		simple_entry['quantity'] = gnucash.GncNumeric(instance=entry.GetQuantity()).to_double()
		#simple_entry['inv_account'] =  entry.GetInvAccount() (swig)
		simple_entry['inv_price'] = gnucash.GncNumeric(instance=entry.GetInvPrice()).to_double()
		simple_entry['discount'] = gnucash.GncNumeric(instance=entry.GetInvDiscount()).to_double()
		simple_entry['discounted_type'] =  entry.GetInvDiscountType()
		simple_entry['discounted_how'] =  entry.GetInvDiscountHow()
		#simple_entry['date'] =  entry.GetInvDiscType()
		#simple_entry['date'] =  entry.GetInvDiscHow()
		simple_entry['inv_taxable'] =  entry.GetInvTaxable()
		simple_entry['inv_tax_included'] =  entry.GetInvTaxIncluded()
		simple_entry['inv_tax_table_override'] =  entry.GetInvTaxTable()
		#simple_entry['bill_account'] =  entry.GetBillAccount()
		simple_entry['bill_price'] = gnucash.GncNumeric(instance=entry.GetBillPrice()).to_double()
		simple_entry['bill_taxable'] =  entry.GetBillTaxable()
		simple_entry['bill_tax_included'] =  entry.GetBillTaxIncluded()
		simple_entry['bill_tax_table'] =  entry.GetBillTaxTable()
		simple_entry['billable'] =  entry.GetBillable()
		#simple_entry['date'] =  entry.GetBillTo()
		simple_entry['bill_payment'] =  entry.GetBillPayment()
		simple_entry['is_open'] =  entry.IsOpen()

		return simple_entry


def accountToDict(account):

	if account is None:
		return None
	else:
		simple_account = {}
		simple_account['name'] =  account.GetName()
		simple_account['guid'] =  account.GetGUID().to_string()
		simple_account['subaccounts'] =  []
		for n, subaccount in enumerate(account.get_children_sorted()):
			simple_account['subaccounts'].append(accountToDict(subaccount))

		#simple_account['commodity'] =  account.GetCommodity()
		#simple_account['book'] =  account.get_book()

		'''

			    
                    'Lookup' : Account,
                    'get_parent' : Account,
                    'get_root' : Account,
                    'nth_child' : Account,
                    'lookup_by_code' : Account,
                    'lookup_by_name' : Account,
                    'lookup_by_full_name' : Account,
                    'FindTransByDesc' : Transaction,
                    'FindSplitByDesc' : Split,
                    'GetBalance' : GncNumeric,
                    'GetClearedBalance' : GncNumeric,
                    'GetReconciledBalance' : GncNumeric,
                    'GetPresentBalance' : GncNumeric,
                    'GetProjectedMinimumBalance' : GncNumeric,
                    'GetBalanceAsOfDate' : GncNumeric,
                    'ConvertBalanceToCurrency' : GncNumeric,
                    'ConvertBalanceToCurrencyAsOfDate' : GncNumeric,
                    'GetBalanceInCurrency' : GncNumeric,
                    'GetClearedBalanceInCurrency' : GncNumeric,
                    'GetReconciledBalanceInCurrency' : GncNumeric,
                    'GetPresentBalanceInCurrency' : GncNumeric,
                    'GetProjectedMinimumBalanceInCurrency' : GncNumeric,
                    'GetBalanceAsOfDateInCurrency' : GncNumeric,
                    'GetBalanceChangeForPeriod' : GncNumeric,
                
           


    Account, { 'GetSplitList': Split,
               'get_children': Account,
               'get_children_sorted': Account,
               'get_descendants': Account,
               'get_descendants_sorted': Account


FROM http://svn.gnucash.org/trac/browser/gnucash/trunk/src/optional/python-bindings/example_scripts/gnc_convenience.py

	    split_list=account.GetSplitList()
	    transaction_list=[]
	    for split in split_list:
	        if type(split) != Split:
	              split = Split(instance=split)
	        transaction=split.GetParent()
	        if not (transaction in transaction_list):       # this check may not be necessary.
	          transaction_list.append(transaction)
	    return transaction_list
	


		'''

		return simple_account