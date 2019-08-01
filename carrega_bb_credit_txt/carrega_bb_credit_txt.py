import re
from locale import atof, setlocale, LC_NUMERIC

#TODO: Estornos ?

REGX = '^\s{7,}(\-?[\d\.,]+)\s{5,}([\d\.,]+)$'

def check_if_line_is_name(a):
	isAllBlankTo10 = a[0:9] == '         '
	at9Is0to9 = bool(re.match('^[0-9]+$', a[9]))
	return isAllBlankTo10 and at9Is0to9

def check_if_is_transaction_line(a):
	a_ = a.strip()
	isLastsDig1 = bool(re.match(',[0-9]+', a_[-3:]))
	isLastsDig2 = bool(re.match(',[0-9]+', a_[66:69]))
	return isLastsDig1 and isLastsDig2

def check_is_transaction_line_rgx(a):
	a = a.strip()
	if 'PGTO' in a:
		return False
	c = re.match(REGX, a[51:])
	return bool(c)

def num_string_br_to_float(s):
	n = s.split(',')
	return float(n[0].replace('.', '')) + float(n[1])/100.0

def get_BRL_USD_values(a):
	a = a.strip()
	text = a[10:50]
	date = a[0:10]
	c = re.match(REGX, a[50:])
	setlocale(LC_NUMERIC, 'pt_BR.utf8') #'Portuguese_Brazil.1252'
	brl = float(atof(c.group(1)))
	usd = float(atof(c.group(2)))
	setlocale(LC_NUMERIC, '')
	return brl, usd, text, date

def get_Taxa_line(a):
	return 'Taxa de' in a

def get_dollar_exchange_rate(a):
	Xpos = a.find('X')
	return float(a[Xpos + 4:Xpos + 4 + 6].replace(',', '.'))

def is_transaction_with_saq_or_saques(a):
	t2 = 'SAQUE' in a
	t3 = 'IOF DIAR ROT PF' in a
	t4 = 'IOF DIAR SAQ PF ' in a
	t5 = 'IOF ADIC SAQ PF ' in a
	return t2 or t3 or t4 or t5

def parse_text_file(fname):
	names = []
	idxLineTaxa = 1e20
	persons_transactions = []
	with open(fname, 'rb') as f:
		for i, line in enumerate(f):
			try:
				a = line.decode('ISO-8859-1')

				# Searching for the "Taxa de"
				if get_Taxa_line(a):
					idxLineTaxa = i
				if i == idxLineTaxa + 3:
					dollarRate = get_dollar_exchange_rate(a)
			

				isNameLine = check_if_line_is_name(a)
				if isNameLine:
					try:
						persons_transactions.append(d) #pylint: disable=E0601
					except NameError:
						pass
					name = a[12:].strip()
					names.append(name)
					d = {'name': name, 'brls': [], 'usds': [], 'entries': []}
					continue

				if isNameLine == False:
					if check_is_transaction_line_rgx(a):
						brl, usd, text, date = get_BRL_USD_values(a)
						d['brls'].append(brl)
						d['usds'].append(usd)
						d['entries'].append({'date': date, 'text': text, 'brl': brl, 'usd': usd})

						# Special transaction to separate
						if is_transaction_with_saq_or_saques(a):
							if 'total-saques' not in d:
								d['total-saques'] = 0.0
							d['total-saques'] += brl

			except (UnicodeDecodeError, IndexError):
				pass

			if not line:
				break

	try:
		persons_transactions.append(d)
	except NameError:
		print('No name found...')

	my_card_info = {
		'dollar-rate': dollarRate,
		'transactions': persons_transactions
	}

	return my_card_info


def calc_total_values(card_info):
	# dollar_exchange_rate = get_dollar_exchange_rate('trash')
	persons_transactions = card_info['transactions']
	dollar_exchange_rate = card_info['dollar-rate']
	for p in persons_transactions:
		brl_simple_sum = sum(p['brls'])
		usd_simple_sum = sum(p['usds'])
		p['brl-simple'] = brl_simple_sum
		p['usd-simple'] = usd_simple_sum
		p['total'] = p['brl-simple'] + p['usd-simple'] * dollar_exchange_rate


def format_print_number(num):
	num_s = '{:.2f}'.format(num)
	# num_s = num_s.replace('.', ',')
	return num_s

def print_expenses(fname, use_comma=False):
	trsctns = parse_text_file(fname)
	f = format_print_number
	calc_total_values(trsctns)
	p_sum = 0.0; brl_sum = 0.0; usd_sum = 0.0
	print('Dollar Exchange Rate \t= {}'.format(f(trsctns['dollar-rate'])))
	for p in trsctns['transactions']:
		print('-------------------------')
		print('NAME: {}'.format(p['name']))
		print('BRL Total : {}'.format(f(p['brl-simple'])))
		print('USD Total : {}'.format(f(p['usd-simple'])))
		print('Total After Convertion: {}'.format(f(p['total'])))
		if 'total-saques' in p:
			print('Total From Saques: {}'.format(f(p['total-saques'])))
		p_sum += p['total']
		brl_sum += p['brl-simple']
		usd_sum += p['usd-simple']
	print('-------------------------')
	print('TOTAL SUM: {:.2f}'.format(p_sum))
	print('TOTAL BRL: {:.2f}'.format(brl_sum))
	print('TOTAL USD: {:.2f}'.format(usd_sum))
