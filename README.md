# Santander Product Recommendation API

**Overview**
- This repo implements a REST API that serves the pretrained ML model created in this notebook: https://www.kaggle.com/sudalairajkumar/when-less-is-more which is part of this Kaggle competition: https://www.kaggle.com/c/santander-product-recommendation/ 

**Getting Started**
- Clone the repo
- pip install -r requirements.txt
- *To run the server:* python server.py
- *To run a sample request:* python request.py

**API prediction endpoint:**
- **Type:** POST
- **URL**: http://127.0.0.1:5000/api/
  
- **Headers**
  - 'content-type': 'application/json'
  - 'Accept-Charset': 'UTF-8'
- **Body**
  -   customer_code: required.
  -   country: optional, possible values (spanish abbreviations): 'LV' , 'BE' , 'BG' , 'BA' , 'BM' , 'BO' , 'JP' , 'JM' , 'BR' , 'BY' , 'BZ' , 'RU' , 'RS' , 'RO' , 'GW' , 'GT' , 'GR' , 'GQ' , 'GE' , 'GB' , 'GA' , 'GN' , 'GM' , 'GI' , 'GH' , 'OM' , 'HR' , 'HU' , 'HK' , 'HN' , 'AD' , 'PR' , 'PT' , 'PY' , 'PA' , 'PE' , 'PK' , 'PH' , 'PL' , 'EE' , 'EG' , 'ZA' , 'EC' , 'AL' , 'VN' , 'ET' , 'ZW' , 'ES' , 'MD' , 'UY' , 'MM' , 'ML' , 'US' , 'MT' , 'MR' , 'UA' , 'MX' , 'IL' , 'FR' , 'MA' , 'FI' , 'NI' , 'NL' , 'NO' , 'NG' , 'NZ' , 'CI' , 'CH' , 'CO' , 'CN' , 'CM' , 'CL' , 'CA' , 'CG' , 'CF' , 'CD' , 'CZ' , 'CR' , 'CU' , 'KE' , 'KH' , 'SV' , 'SK' , 'KR' , 'KW' , 'SN' , 'SL' , 'KZ' , 'SA' , 'SG' , 'SE' , 'DO' , 'DJ' , 'DK' , 'DE' , 'DZ' , 'MK' , 'LB' , 'TW' , 'TR' , 'TN' , 'LT' , 'LU' , 'TH' , 'TG' , 'LY' , 'AE' , 'VE' , 'IS' , 'IT' , 'AO' , 'AR' , 'AU' , 'AT' , 'IN' , 'IE' , 'QA' , 'MZ'
  -   gender: optional: possible values: 'M' or 'F'
  -   age: optional, range: 20-90 
  -   seniority: optional, range: 0-256
  -   relation_type: optional, possible values: 'A' (active), 'I' (inactive), 'P' (former customer) or 'R' (Potential)
  -   activity_index: optional, possible values: '1' (active customer) or '0' (inactive customer)
  -   gross_income: optional, range: 0-1500000
  -   segmentation: optional, possible values: '1' (VIP), '2' (Individuals), '3' (college graduated)
- **Sample Response**
    {
    "code": 200,
    "products": [
      "Saving_Account",
      "Particular_Account",
      "Payroll",
      "Short_term_deposits",
      "Securities",
      "Home_Account",
      "Payroll_Account"
    ]
   }
 - **Sample Error Response**
    {
  "code": 422,
  "message": "customer code must be provided"
  }

