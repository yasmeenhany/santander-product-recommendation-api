from flask import Flask, request, redirect, url_for, flash, jsonify, abort
import numpy as np
import pickle
import json
import csv
import pandas as pd
from collections import OrderedDict
import xgboost as xgb
app = Flask(__name__)

mapping_dict = {
'ind_empleado'  : {-99:0, 'N':1, 'B':2, 'F':3, 'A':4, 'S':5},
'sexo'          : {'M':0, 'F':1, -99:2},
'ind_nuevo'     : {'0':0, '1':1, -99:2},
'indrel'        : {'1':0, '99':1, -99:2},
'indrel_1mes'   : {-99:0, '1.0':1, '1':1, '2.0':2, '2':2, '3.0':3, '3':3, '4.0':4, '4':4, 'P':5},
'tiprel_1mes'   : {-99:0, 'I':1, 'A':2, 'P':3, 'R':4, 'N':5},
'indresi'       : {-99:0, 'S':1, 'N':2},
'indext'        : {-99:0, 'S':1, 'N':2},
'conyuemp'      : {-99:0, 'S':1, 'N':2},
'indfall'       : {-99:0, 'S':1, 'N':2},
'tipodom'       : {-99:0, '1':1},
'ind_actividad_cliente' : {'0':0, '1':1, -99:2},
'segmento'      : {'2':0, '3':1, '1':2, -99:2},
'pais_residencia' : {'LV': 102, 'BE': 12, 'BG': 50, 'BA': 61, 'BM': 117, 'BO': 62, 'JP': 82, 'JM': 116, 'BR': 17, 'BY': 64, 'BZ': 113, 'RU': 43, 'RS': 89, 'RO': 41, 'GW': 99, 'GT': 44, 'GR': 39, 'GQ': 73, 'GE': 78, 'GB': 9, 'GA': 45, 'GN': 98, 'GM': 110, 'GI': 96, 'GH': 88, 'OM': 100, 'HR': 67, 'HU': 106, 'HK': 34, 'HN': 22, 'AD': 35, 'PR': 40, 'PT': 26, 'PY': 51, 'PA': 60, 'PE': 20, 'PK': 84, 'PH': 91, 'PL': 30, 'EE': 52, 'EG': 74, 'ZA': 75, 'EC': 19, 'AL': 25, 'VN': 90, 'ET': 54, 'ZW': 114, 'ES': 0, 'MD': 68, 'UY': 77, 'MM': 94, 'ML': 104, 'US': 15, 'MT': 118, 'MR': 48, 'UA': 49, 'MX': 16, 'IL': 42, 'FR': 8, 'MA': 38, 'FI': 23, 'NI': 33, 'NL': 7, 'NO': 46, 'NG': 83, 'NZ': 93, 'CI': 57, 'CH': 3, 'CO': 21, 'CN': 28, 'CM': 55, 'CL': 4, 'CA': 2, 'CG': 101, 'CF': 109, 'CD': 112, 'CZ': 36, 'CR': 32, 'CU': 72, 'KE': 65, 'KH': 95, 'SV': 53, 'SK': 69, 'KR': 87, 'KW': 92, 'SN': 47, 'SL': 97, 'KZ': 111, 'SA': 56, 'SG': 66, 'SE': 24, 'DO': 11, 'DJ': 115, 'DK': 76, 'DE': 10, 'DZ': 80, 'MK': 105, -99: 1, 'LB': 81, 'TW': 29, 'TR': 70, 'TN': 85, 'LT': 103, 'LU': 59, 'TH': 79, 'TG': 86, 'LY': 108, 'AE': 37, 'VE': 14, 'IS': 107, 'IT': 18, 'AO': 71, 'AR': 13, 'AU': 63, 'AT': 6, 'IN': 31, 'IE': 5, 'QA': 58, 'MZ': 27},
'canal_entrada' : {'013': 49, 'KHP': 160, 'KHQ': 157, 'KHR': 161, 'KHS': 162, 'KHK': 10, 'KHL': 0, 'KHM': 12, 'KHN': 21, 'KHO': 13, 'KHA': 22, 'KHC': 9, 'KHD': 2, 'KHE': 1, 'KHF': 19, '025': 159, 'KAC': 57, 'KAB': 28, 'KAA': 39, 'KAG': 26, 'KAF': 23, 'KAE': 30, 'KAD': 16, 'KAK': 51, 'KAJ': 41, 'KAI': 35, 'KAH': 31, 'KAO': 94, 'KAN': 110, 'KAM': 107, 'KAL': 74, 'KAS': 70, 'KAR': 32, 'KAQ': 37, 'KAP': 46, 'KAW': 76, 'KAV': 139, 'KAU': 142, 'KAT': 5, 'KAZ': 7, 'KAY': 54, 'KBJ': 133, 'KBH': 90, 'KBN': 122, 'KBO': 64, 'KBL': 88, 'KBM': 135, 'KBB': 131, 'KBF': 102, 'KBG': 17, 'KBD': 109, 'KBE': 119, 'KBZ': 67, 'KBX': 116, 'KBY': 111, 'KBR': 101, 'KBS': 118, 'KBP': 121, 'KBQ': 62, 'KBV': 100, 'KBW': 114, 'KBU': 55, 'KCE': 86, 'KCD': 85, 'KCG': 59, 'KCF': 105, 'KCA': 73, 'KCC': 29, 'KCB': 78, 'KCM': 82, 'KCL': 53, 'KCO': 104, 'KCN': 81, 'KCI': 65, 'KCH': 84, 'KCK': 52, 'KCJ': 156, 'KCU': 115, 'KCT': 112, 'KCV': 106, 'KCQ': 154, 'KCP': 129, 'KCS': 77, 'KCR': 153, 'KCX': 120, 'RED': 8, 'KDL': 158, 'KDM': 130, 'KDN': 151, 'KDO': 60, 'KDH': 14, 'KDI': 150, 'KDD': 113, 'KDE': 47, 'KDF': 127, 'KDG': 126, 'KDA': 63, 'KDB': 117, 'KDC': 75, 'KDX': 69, 'KDY': 61, 'KDZ': 99, 'KDT': 58, 'KDU': 79, 'KDV': 91, 'KDW': 132, 'KDP': 103, 'KDQ': 80, 'KDR': 56, 'KDS': 124, 'K00': 50, 'KEO': 96, 'KEN': 137, 'KEM': 155, 'KEL': 125, 'KEK': 145, 'KEJ': 95, 'KEI': 97, 'KEH': 15, 'KEG': 136, 'KEF': 128, 'KEE': 152, 'KED': 143, 'KEC': 66, 'KEB': 123, 'KEA': 89, 'KEZ': 108, 'KEY': 93, 'KEW': 98, 'KEV': 87, 'KEU': 72, 'KES': 68, 'KEQ': 138, -99: 6, 'KFV': 48, 'KFT': 92, 'KFU': 36, 'KFR': 144, 'KFS': 38, 'KFP': 40, 'KFF': 45, 'KFG': 27, 'KFD': 25, 'KFE': 148, 'KFB': 146, 'KFC': 4, 'KFA': 3, 'KFN': 42, 'KFL': 34, 'KFM': 141, 'KFJ': 33, 'KFK': 20, 'KFH': 140, 'KFI': 134, '007': 71, '004': 83, 'KGU': 149, 'KGW': 147, 'KGV': 43, 'KGY': 44, 'KGX': 24, 'KGC': 18, 'KGN': 11}
}
cat_cols = list(mapping_dict.keys())
target_cols = ['Saving_Account','Guarantees','Current_Accounts','Derivada_Account','Payroll_Account','Junior_Account','Mas_particular_Account','Particular_Account','Particular_Plus_Account','Short_term_deposits','Medium_term_deposits','Long_term_deposits','e_account','Funds','Mortgage','Pensions','Loans','Taxes','Credit_Card','Securities','Home_Account','Payroll','Pensions','Direct_Debit']
# target_cols = target_cols[2:]
@app.errorhandler(500)
def resource_not_found(e):
    return jsonify(error=str(e)), 400
def getTarget(row):
	tlist = []
	for col in target_cols:
		if row[col].strip() in ['', 'NA']:
			target = 0
		else:
			target = int(float(row[col]))
		tlist.append(target)
	return tlist

def getIndex(row, col):
	val = row[col].strip()
	if val not in ['','NA']:
		ind = mapping_dict[col][val]
	else:
		ind = mapping_dict[col][-99]
	return ind

def getAge(row):
	mean_age = 40.
	min_age = 20.
	max_age = 90.
	range_age = max_age - min_age
	age = row['age'].strip()
	if age == 'NA' or age == '':
		age = mean_age
	else:
		age = float(age)
		if age < min_age:
			age = min_age
		elif age > max_age:
			age = max_age
	return round( (age - min_age) / range_age, 4)

def getCustSeniority(row):
	min_value = 0.
	max_value = 256.
	range_value = max_value - min_value
	missing_value = 0.
	cust_seniority = row['antiguedad'].strip()
	if cust_seniority == 'NA' or cust_seniority == '':
		cust_seniority = missing_value
	else:
		cust_seniority = float(cust_seniority)
		if cust_seniority < min_value:
			cust_seniority = min_value
		elif cust_seniority > max_value:
			cust_seniority = max_value
	return round((cust_seniority-min_value) / range_value, 4)

def getRent(row):
	min_value = 0.
	max_value = 1500000.
	range_value = max_value - min_value
	missing_value = 101850.
	rent = row['renta'].strip()
	if rent == 'NA' or rent == '':
		rent = missing_value
	else:
		rent = float(rent)
		if rent < min_value:
			rent = min_value
		elif rent > max_value:
			rent = max_value
	return round((rent-min_value) / range_value, 6)

def processData(row, cust_dict):
	x_vars_list = []
	y_vars_list = []
	# for row in csv.DictReader(in_file_name):
	# use only the four months as specified by breakfastpirate #
	# if row['fecha_dato'] not in ['2015-05-28', '2015-06-28', '2016-05-28', '2016-06-28']:
	# 	continue

	cust_id = int(row['ncodpers'])
	if row['fecha_dato'] in ['2015-05-28', '2016-05-28']:	
		target_list = getTarget(row)
		cust_dict[cust_id] =  target_list[:]
		# continue

	x_vars = []
	for col in cat_cols:
		x_vars.append( getIndex(row, col) )
	x_vars.append( getAge(row) )
	x_vars.append( getCustSeniority(row) )
	x_vars.append( getRent(row) )

	if row['fecha_dato'] == '2016-06-28':
		prev_target_list = cust_dict.get(cust_id, [0]*22)
		x_vars_list.append(x_vars + prev_target_list)
	elif row['fecha_dato'] == '2015-06-28':
		prev_target_list = cust_dict.get(cust_id, [0]*22)
		target_list = getTarget(row)
		new_products = [max(x1 - x2,0) for (x1, x2) in zip(target_list, prev_target_list)]
		if sum(new_products) > 0:
			for ind, prod in enumerate(new_products):
				if prod>0:
					assert len(prev_target_list) == 22
					x_vars_list.append(x_vars+prev_target_list)
					y_vars_list.append(ind)

	return x_vars_list, y_vars_list, cust_dict

def prepareData(body):
	if not "customer_code" or len(body["customer_code"]) == 0:
		abort(400, description="customer code must be provided")
	skeleton = OrderedDict([('fecha_dato', '2016-06-28'), ('ncodpers', ''), ('ind_empleado', ''), ('pais_residencia', ''), ('sexo', ''), ('age', ''), ('fecha_alta', ''), ('ind_nuevo', ''), ('antiguedad', ''), ('indrel', ' '), ('ult_fec_cli_1t', ''), ('indrel_1mes', ''), ('tiprel_1mes', ''), ('indresi', ''), ('indext', ''), ('conyuemp', ''), ('canal_entrada', ''), ('indfall', ''), ('tipodom', ''), ('cod_prov', ''), ('nomprov', ''), ('ind_actividad_cliente', ''), ('renta', ''), ('segmento', '')])	
	if "customer_code" in body:
		skeleton['ncodpers'] = body["customer_code"]
	if "country" in body:
		skeleton['pais_residencia'] = body["country"]
	if "gender" in body:
		skeleton['sexo'] = body["gender"]
	if "age" in body:
		skeleton['age'] = body["age"]
	if "seniority" in body:
		skeleton['antiguedad'] = body["seniority"]
	if "relation_type" in body:
		skeleton['tiprel_1mes'] = body["relation_type"]
	if "activity_index" in body:
		skeleton['ind_actividad_cliente'] = body["activity_index"]
	if "gross_income" in body:
		skeleton['renta'] = body["gross_income"]
	if "segmentation" in body:
		skeleton['segmento'] = body["segmentation"]
	return skeleton

def predict(data):
	x_vars_list, _, _ = processData(data,{})
	test_X = np.array(x_vars_list)
	processed_data = xgb.DMatrix(test_X)
	preds = np.array(model.predict(processed_data))
	preds = np.argsort(preds, axis=1)
	preds = np.fliplr(preds)[:,:7]
	target_cols = ['Saving_Account','Guarantees','Current_Accounts','Derivada_Account','Payroll_Account','Junior_Account','Mas_particular_Account','Particular_Account','Particular_Plus_Account','Short_term_deposits','Medium_term_deposits','Long_term_deposits','e_account','Funds','Mortgage','Pensions','Loans','Taxes','Credit_Card','Securities','Home_Account','Payroll','Pensions','Direct_Debit']
	# target_cols = target_cols[2:]
	target_cols = np.array(target_cols)
	final_preds = [" ".join(list(target_cols[pred])) for pred in preds]
	return jsonify(final_preds[0].split(" "))

@app.route('/api/', methods=['POST'])
def makecalc():
	body = request.get_json()
	data = prepareData(body)
	response = predict(data)
	return response
	

if __name__ == '__main__':
	modelfile = 'model.pkl'
	model = pickle.load(open(modelfile, 'rb'))
	app.run(debug=True, host='127.0.0.1')