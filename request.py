import requests
import json

url = 'http://127.0.0.1:5000/api/'

# data = [[14.34, 1.68, 2.7, 25.0, 98.0, 2.8, 1.31, 0.53, 2.7, 13.0, 0.57, 1.96, 660.0]]
data = {
    "customer_code":"70" ,
    # 'LV' , 'BE' , 'BG' , 'BA' , 'BM' , 'BO' , 'JP' , 'JM' , 'BR' , 'BY' , 'BZ' , 'RU' , 'RS' , 'RO' , 'GW' , 'GT' , 'GR' , 'GQ' , 'GE' , 'GB' , 'GA' , 'GN' , 'GM' , 'GI' , 'GH' , 'OM' , 'HR' , 'HU' , 'HK' , 'HN' , 'AD' , 'PR' , 'PT' , 'PY' , 'PA' , 'PE' , 'PK' , 'PH' , 'PL' , 'EE' , 'EG' , 'ZA' , 'EC' , 'AL' , 'VN' , 'ET' , 'ZW' , 'ES' , 'MD' , 'UY' , 'MM' , 'ML' , 'US' , 'MT' , 'MR' , 'UA' , 'MX' , 'IL' , 'FR' , 'MA' , 'FI' , 'NI' , 'NL' , 'NO' , 'NG' , 'NZ' , 'CI' , 'CH' , 'CO' , 'CN' , 'CM' , 'CL' , 'CA' , 'CG' , 'CF' , 'CD' , 'CZ' , 'CR' , 'CU' , 'KE' , 'KH' , 'SV' , 'SK' , 'KR' , 'KW' , 'SN' , 'SL' , 'KZ' , 'SA' , 'SG' , 'SE' , 'DO' , 'DJ' , 'DK' , 'DE' , 'DZ' , 'MK' , - , 'LB' , 'TW' , 'TR' , 'TN' , 'LT' , 'LU' , 'TH' , 'TG' , 'LY' , 'AE' , 'VE' , 'IS' , 'IT' , 'AO' , 'AR' , 'AU' , 'AT' , 'IN' , 'IE' , 'QA' , 'MZ'
    "country": "ES",
    #F or M
    "gender": "M",
    #range:20-90
    "age": "35",
    #range=0-256
    "seniority":"8",
    # Customer relation type at the beginning of the month, A (active), I (inactive), P (former customer),R (Potential)
    "relation_type": "A",
    # Activity index (1, active customer; 0, inactive customer)
    "activity_index": "1",
    #range: 0-1500000
    "gross_income": "12000",
    # segmentation: 1 = VIP, 2 =Individuals, 3 = college graduated
    "segmentation": "3"

}
j_data = json.dumps(data)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=j_data, headers=headers)
print(r, r.text)