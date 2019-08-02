
import pytest
#from parse_bb_credit import *
import carrega_bb_credit_txt as parse_bb_credit

#--------------------------------------------
# 	 PARSE TXT FILE 	 
#--------------------------------------------

@pytest.fixture()
def my_file():
	return 'data/OUROCARD_VISA_INFINITE-Jul_18.txt'

def test_check_if_is_name_line():
	s = '         1 - LIVIA M QUINTANILHA                     \r\n'
	r = parse_bb_credit.check_if_line_is_name(s)
	assert(r)


def test_check_if_is_name_line2():
	s = '         2 - TEREZA C M MARQUES                      \r\n'
	r = parse_bb_credit.check_if_line_is_name(s)
	assert(r)


def test_check_if_is_name_line3():
	s = '         Restaurantes                                \r\n'
	r = parse_bb_credit.check_if_line_is_name(s)
	assert(r == False)

def test_check_if_is_transaction_line():
	s = '27.05.2018CHEF EXPRESS S.P.A.    FIUMICINO     IT                0,00        1,30\r\n'
	r = parse_bb_credit.check_if_is_transaction_line(s)
	assert(r)

def test_check_if_is_transaction_line2():
	s = '11.05.2018CEA BAR 530   PARC 02/03 RIO DE JANEIBR               19,99        0,00\r\n'
	r = parse_bb_credit.check_if_is_transaction_line(s)
	assert(r)

def test_check_if_is_transaction_line3():
	s = '         SubTotal                                           2.471,18        0,00\r\n'
	r = parse_bb_credit.check_if_is_transaction_line(s)
	assert(r == False)


def test_get_brl_usd():
	s = '27.05.2018CHEF EXPRESS S.P.A.    FIUMICINO     IT                0,00        1,30\r\n'
	r = parse_bb_credit.get_BRL_USD_values(s)
	assert(r[0] < 0.001)
	assert(r[1] < 1.31)


def test_get_brl_usd2():
	s = '11.05.2018CEA BAR 530   PARC 02/03 RIO DE JANEIBR               19,99        0,00\r\n'
	r = parse_bb_credit.get_BRL_USD_values(s)
	assert(r[0] < 20.00)
	assert(r[1] < 0.01)

def test_read_txt(my_file):
	parse_bb_credit.parse_text_file(my_file)
	assert True

#--------------------------------------------
# 	 GET ALL FROM THE TXT FILE 	 
#--------------------------------------------
def test_transactions_smoke(my_file):
	my_card_info = parse_bb_credit.parse_text_file(my_file)
	assert True

def test_transactions_first(my_file):
	my_card_info = parse_bb_credit.parse_text_file(my_file)
	ptrns = my_card_info['transactions'][0]
	assert ptrns['name'].split(' ')[0] == 'LIVIA'
	assert len(ptrns['brls']) >= 69
	assert len(ptrns['brls']) >= 69

def test_transactions_sec(my_file):
	my_card_info = parse_bb_credit.parse_text_file(my_file)
	ptrns = my_card_info['transactions'][1]
	assert ptrns['name'].split(' ')[0] == 'TEREZA'
	assert len(ptrns['brls']) == 71
	assert len(ptrns['usds']) == 71

def test_transactions_third(my_file):
	my_card_info = parse_bb_credit.parse_text_file(my_file)
	ptrns = my_card_info['transactions'][2]
	assert ptrns['name'].split(' ')[0] == 'CAIO'
	assert len(ptrns['brls']) == 39
	assert len(ptrns['usds']) == 39

def test_dollar_rate_Taxa_line():
	s = '  Compras/     Outros                      Saldo       Taxa de         Saldo    '
	r = parse_bb_credit.get_Taxa_line(s)
	assert(r)

def test_get_exchange_rate():
	s = '    738,19 -      47,13 +       0,00 =      785,32   X   3,9230 =       3.080,81'
	r = parse_bb_credit.get_dollar_exchange_rate(s)
	assert(r == 3.923)

def test_saq_transaction():
	s = '01.06.2018IOF DIAR SAQ PF REF.05/18            BR                0,33        0,00'
	r = parse_bb_credit.is_transaction_with_saq_or_saques(s)
	assert(r)

def test_format_print_number():
	num = parse_bb_credit.format_print_number(2004322409.4324)
	assert(num == '2004322409,43')


def test_check_is_transaction_line_rgx():
	s = '08.06.2018SAQUE AGEN.5864 AV.TEIXEIRA E SOUZA  -RJ            1.000,00        0,00'
	r = parse_bb_credit.check_is_transaction_line_rgx(s)
	assert(r == True)
	# assert(r[1] == '1.000,00')
	# assert(r[2] == '0,00')


def test_check_is_transaction_line_rgx2():
	s = '11.05.2018CEA BAR 530   PARC 02/03 RIO DE JANEIBR               19,99        0,00\r\n'
	r = parse_bb_credit.check_is_transaction_line_rgx(s)
	assert(r == True)
	# assert(r == '19,99')
	# assert(r == '0,00')


def test_check_is_transaction_line_rgx3():
	s = '10.05.2018ESTORNO ENCARGOS FINANC ROTATIVO     BR              48,02        0,00\r\n'
	r = parse_bb_credit.check_is_transaction_line_rgx(s)
	assert(r == True)

def test_check_is_transaction_line_rgx4():
	s = '27.06.2018ENCARGOS DE SAQUES                                   555,01        0,00\r\n'
	r = parse_bb_credit.check_is_transaction_line_rgx(s)
	assert(r == True)

def test_check_is_transaction_line_values():
	s1 = '08.06.2018SAQUE AGEN.5864 AV.TEIXEIRA E SOUZA  -RJ            1.000,00        0,00'
	s2 = '27.06.2018ENCARGOS DE SAQUES                                   555,01        0,00\r\n'
	r1 = parse_bb_credit.get_BRL_USD_values(s1)
	r2 = parse_bb_credit.get_BRL_USD_values(s2)
	assert(r1[0] == 1000.00)
	assert(r1[1] == 0.0)
	assert(r2[0] == 555.01)
	assert(r2[1] == 0.0)

#--------------------------------------------
# 	 EXTERNAL UTILITIES TEST 	 
#--------------------------------------------
@pytest.fixture()
def my_card_info(my_file):
	my_card_info = parse_bb_credit.parse_text_file(my_file)
	return my_card_info

def test_summations(my_card_info):
	parse_bb_credit.calc_total_values(my_card_info)
	hasattr(my_card_info['transactions'][0], 'brl-simple')
	hasattr(my_card_info['transactions'][0], 'usd-simple')
	hasattr(my_card_info['transactions'][0], 'total')
	assert(True)


#--------------------------------------------
# 	 ACCEPTANCE TEST WITH ESTILO VISA 	 
#--------------------------------------------
@pytest.fixture()
def my_vestilo():
	return 'data/OUROCARD_PLATINUM_ESTILO_VISA-Jul_18.txt'

def test_v_estilo(my_vestilo):
	my_card_info = parse_bb_credit.parse_text_file(my_vestilo)
	ptrns = my_card_info['transactions'][0]
	assert ptrns['name'].split(' ')[0] == ''
	assert len(ptrns['brls']) >= 13
	assert len(ptrns['usds']) >= 13


def test_print_estilo(my_vestilo):
	parse_bb_credit.print_expenses(my_vestilo)



def main():
	parse_bb_credit.print_expenses('./data/OUROCARD_VISA_INFINITE-Ago_18.txt')

	return

if __name__ == '__main__':
	main()



