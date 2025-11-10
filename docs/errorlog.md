2025-11-10T07:13:49.989995402Z INFO: Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
2025-11-10T07:13:50.939919811Z INFO: 127.0.0.1:35284 - "HEAD / HTTP/1.1" 405 Method Not Allowed
2025-11-10T07:13:51.208653605Z ==> Your service is live 🎉
2025-11-10T07:13:51.408314651Z ==>
2025-11-10T07:13:51.601022257Z ==> ///////////////////////////////////////////////////////////
2025-11-10T07:13:51.811787481Z ==>
2025-11-10T07:13:52.007269737Z ==> Available at your primary URL https://evara-8w6h.onrender.com
2025-11-10T07:13:52.198668363Z ==>
2025-11-10T07:13:52.391543359Z ==> ///////////////////////////////////////////////////////////
2025-11-10T07:13:54.893298793Z INFO: 35.230.45.39:0 - "GET / HTTP/1.1" 200 OK
2025-11-10T07:14:04.901018094Z 2025-11-10 07:14:04 - INFO - ⏰ Reminder check at 12:44:04 PM IST - Found 0 pending reminder(s)
2025-11-10T07:14:13.577613383Z 2025-11-10 07:14:13 - INFO - ================================================================================
2025-11-10T07:14:13.577635723Z 2025-11-10 07:14:13 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:14:13.577734376Z 2025-11-10 07:14:13 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JGQjM4MDYxNUZDQTBDQTNCQkUA', 'timestamp': '1762758852', 'text': {'body': 'set reminder for 12:55PM IST today.'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:13.577843478Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JGQjM4MDYxNUZDQTBDQTNCQkUA', 'timestamp': '1762758852', 'text': {'body': 'set reminder for 12:55PM IST today.'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:13.577866818Z 2025-11-10 07:14:13 - INFO - From: whatsapp:917092724850
2025-11-10T07:14:13.577986061Z 2025-11-10 07:14:13 - INFO - Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JGQjM4MDYxNUZDQTBDQTNCQkUA
2025-11-10T07:14:13.577993691Z 2025-11-10 07:14:13 - INFO - Body: set reminder for 12:55PM IST today....
2025-11-10T07:14:13.578126784Z 2025-11-10 07:14:13 - INFO - 🤖 Processing message from whatsapp:917092724850: set reminder for 12:55PM IST today....
2025-11-10T07:14:15.85697587Z 2025-11-10 07:14:15 - INFO - 📊 Intent: reminder (confidence: 0.98)
2025-11-10T07:14:15.857084382Z 2025-11-10 07:14:15 - INFO - 🔧 Executing tool for intent: reminder
2025-11-10T07:14:15.857195864Z 2025-11-10 07:14:15 - INFO - ⏰ Reminder requested: None at 12:55PM (country: India, location: None)
2025-11-10T07:14:17.143558314Z 2025-11-10 07:14:17 - INFO - Created daily backup: /opt/render/project/src/taskflow/data/backups/user_memory_2025-11-10.json
2025-11-10T07:14:17.144090124Z 2025-11-10 07:14:17 - INFO - ✅ Generated response: Okay! Reminder set for 12:55 PM IST today. 👍 You have 1 active reminder now....
2025-11-10T07:14:17.144182136Z 2025-11-10 07:14:17 - INFO - 📤 Sending message via Meta WhatsApp to whatsapp:917092724850
2025-11-10T07:14:17.144285048Z 2025-11-10 07:14:17 - INFO - 📤 Sending Meta WhatsApp message to 917092724850
2025-11-10T07:14:18.909078053Z 2025-11-10 07:14:18 - INFO - ✅ Message sent successfully. Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMkJFMEIxNEZDQkM1NDQxQzU5AA==
2025-11-10T07:14:18.909104853Z 2025-11-10 07:14:18 - INFO - ✅ Message processed and response sent successfully
2025-11-10T07:14:18.909110534Z 2025-11-10 07:14:18 - INFO - ================================================================================
2025-11-10T07:14:18.909115424Z INFO: 173.252.127.15:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:14:19.887628936Z 2025-11-10 07:14:19 - INFO - ================================================================================
2025-11-10T07:14:19.887677077Z 2025-11-10 07:14:19 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:14:19.887794599Z 2025-11-10 07:14:19 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMkJFMEIxNEZDQkM1NDQxQzU5AA==', 'status': 'sent', 'timestamp': '1762758859', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:19.887882091Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMkJFMEIxNEZDQkM1NDQxQzU5AA==', 'status': 'sent', 'timestamp': '1762758859', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:19.887888421Z 2025-11-10 07:14:19 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:14:19.888094325Z INFO: 173.252.79.8:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:14:19.901744444Z 2025-11-10 07:14:19 - INFO - ⏰ Reminder check at 12:44:19 PM IST - Found 1 pending reminder(s)
2025-11-10T07:14:19.901873506Z 2025-11-10 07:14:19 - INFO - 📋 Reminder 0ada2c99... for 917092724850: Due at 12:55:00 PM, Time diff: -640.1s, Status: waiting
2025-11-10T07:14:20.557946824Z 2025-11-10 07:14:20 - INFO - ================================================================================
2025-11-10T07:14:20.558030955Z 2025-11-10 07:14:20 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:14:20.558165528Z 2025-11-10 07:14:20 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMkJFMEIxNEZDQkM1NDQxQzU5AA==', 'status': 'delivered', 'timestamp': '1762758859', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:20.55824346Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMkJFMEIxNEZDQkM1NDQxQzU5AA==', 'status': 'delivered', 'timestamp': '1762758859', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:20.55825173Z 2025-11-10 07:14:20 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:14:20.558469364Z INFO: 173.252.127.36:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:14:22.003743784Z 2025-11-10 07:14:22 - INFO - ================================================================================
2025-11-10T07:14:22.003825276Z 2025-11-10 07:14:22 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:14:22.003936998Z 2025-11-10 07:14:22 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMkJFMEIxNEZDQkM1NDQxQzU5AA==', 'status': 'read', 'timestamp': '1762758861', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:22.004091931Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMkJFMEIxNEZDQkM1NDQxQzU5AA==', 'status': 'read', 'timestamp': '1762758861', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:22.004101891Z 2025-11-10 07:14:22 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:14:22.004302785Z INFO: 173.252.127.1:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:14:34.901765037Z 2025-11-10 07:14:34 - INFO - ⏰ Reminder check at 12:44:34 PM IST - Found 1 pending reminder(s)
2025-11-10T07:14:34.901870939Z 2025-11-10 07:14:34 - INFO - 📋 Reminder 0ada2c99... for 917092724850: Due at 12:55:00 PM, Time diff: -625.1s, Status: waiting
2025-11-10T07:14:45.305338826Z 2025-11-10 07:14:45 - INFO - ================================================================================
2025-11-10T07:14:45.305441538Z 2025-11-10 07:14:45 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:14:45.30555081Z 2025-11-10 07:14:45 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JDRTEwMzc1Nzk2OTM1OTgxQUMA', 'timestamp': '1762758883', 'text': {'body': 'search flights from chennai to bangalore on Dec 15'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:45.305638552Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JDRTEwMzc1Nzk2OTM1OTgxQUMA', 'timestamp': '1762758883', 'text': {'body': 'search flights from chennai to bangalore on Dec 15'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:45.305643802Z 2025-11-10 07:14:45 - INFO - From: whatsapp:917092724850
2025-11-10T07:14:45.305700194Z 2025-11-10 07:14:45 - INFO - Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JDRTEwMzc1Nzk2OTM1OTgxQUMA
2025-11-10T07:14:45.305737634Z 2025-11-10 07:14:45 - INFO - Body: search flights from chennai to bangalore on Dec 15...
2025-11-10T07:14:45.305833866Z 2025-11-10 07:14:45 - INFO - 🤖 Processing message from whatsapp:917092724850: search flights from chennai to bangalore on Dec 15...
2025-11-10T07:14:46.972552511Z 2025-11-10 07:14:46 - INFO - 📊 Intent: flight_search (confidence: 0.95)
2025-11-10T07:14:46.972631302Z 2025-11-10 07:14:46 - INFO - 🔧 Executing tool for intent: flight_search
2025-11-10T07:14:46.972726074Z 2025-11-10 07:14:46 - INFO - 🔍 Flight search entities - Origin: chennai, Destination: bangalore, Date: Dec 15
2025-11-10T07:14:46.972797406Z 2025-11-10 07:14:46 - INFO - ✈️ Flight search: chennai -> bangalore on Dec 15
2025-11-10T07:14:46.972880257Z 2025-11-10 07:14:46 - INFO - 📅 Parsing date: 'Dec 15'
2025-11-10T07:14:47.743544981Z 2025-11-10 07:14:47 - INFO - ✅ Parsed date: 'Dec 15' → 2025-12-15
2025-11-10T07:14:47.743662164Z 2025-11-10 07:14:47 - INFO - 🔍 Calling SerpAPI: chennai -> bangalore on 2025-12-15
2025-11-10T07:14:47.743745575Z 2025-11-10 07:14:47 - INFO - 🔄 Converting city names to airport codes...
2025-11-10T07:14:47.743754735Z 2025-11-10 07:14:47 - INFO - Origin: 'chennai'
2025-11-10T07:14:48.381654632Z 2025-11-10 07:14:48 - INFO - ✅ Converted 'chennai' to airport code: MAA
2025-11-10T07:14:48.381739134Z 2025-11-10 07:14:48 - INFO - Origin code: MAA
2025-11-10T07:14:48.381779195Z 2025-11-10 07:14:48 - INFO - Destination: 'bangalore'
2025-11-10T07:14:49.030582294Z 2025-11-10 07:14:49 - INFO - ✅ Converted 'bangalore' to airport code: BLR
2025-11-10T07:14:49.030609054Z 2025-11-10 07:14:49 - INFO - Destination code: BLR
2025-11-10T07:14:49.030725067Z 2025-11-10 07:14:49 - INFO - ✈️ SerpAPI Request: MAA -> BLR on 2025-12-15
2025-11-10T07:14:49.030806328Z 2025-11-10 07:14:49 - INFO - 📋 Full params: {'engine': 'google_flights', 'api_key': '123756fc070a2d2a5567893e7b213edbf2ab302d595bf0a48bfd9b12744ec23e', 'departure_id': 'MAA', 'arrival_id': 'BLR', 'outbound_date': '2025-12-15', 'currency': 'INR', 'hl': 'en', 'gl': 'in'}
2025-11-10T07:14:49.187942632Z 2025-11-10 07:14:49 - INFO - 📡 Sending request to SerpAPI...
2025-11-10T07:14:49.526895373Z 2025-11-10 07:14:49 - INFO - 📡 SerpAPI Status Code: 400
2025-11-10T07:14:49.526924394Z 2025-11-10 07:14:49 - INFO - 📡 SerpAPI request URL: https://serpapi.com/search?engine=google_flights&api_key=123756fc070a2d2a5567893e7b213edbf2ab302d595bf0a48bfd9b12744ec23e&departure_id=MAA&arrival_id=BLR&outbound_date=2025-12-15&currency=INR&hl=en&gl=in
2025-11-10T07:14:49.527087348Z 2025-11-10 07:14:49 - ERROR - SerpAPI 400 error: `return_date` is required if `type` is `1` (Round trip).
2025-11-10T07:14:49.527170849Z 2025-11-10 07:14:49 - ERROR - Request params: {'engine': 'google_flights', 'api_key': '123756fc070a2d2a5567893e7b213edbf2ab302d595bf0a48bfd9b12744ec23e', 'departure_id': 'MAA', 'arrival_id': 'BLR', 'outbound_date': '2025-12-15', 'currency': 'INR', 'hl': 'en', 'gl': 'in'}
2025-11-10T07:14:50.533670062Z 2025-11-10 07:14:50 - INFO - ✅ Generated response: I couldn't find flights from Chennai (MAA) to Bangalore (BLR) on December 15, 2025. 😔 The route migh...
2025-11-10T07:14:50.533748993Z 2025-11-10 07:14:50 - INFO - 📤 Sending message via Meta WhatsApp to whatsapp:917092724850
2025-11-10T07:14:50.533811245Z 2025-11-10 07:14:50 - INFO - 📤 Sending Meta WhatsApp message to 917092724850
2025-11-10T07:14:50.600637687Z 2025-11-10 07:14:50 - INFO - ⏰ Reminder check at 12:44:50 PM IST - Found 1 pending reminder(s)
2025-11-10T07:14:50.600720629Z 2025-11-10 07:14:50 - INFO - 📋 Reminder 0ada2c99... for 917092724850: Due at 12:55:00 PM, Time diff: -609.4s, Status: waiting
2025-11-10T07:14:51.243178619Z 2025-11-10 07:14:51 - INFO - ✅ Message sent successfully. Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRDgyOTQ4OTNFOTUyMUQ0QTlEAA==
2025-11-10T07:14:51.243361732Z 2025-11-10 07:14:51 - INFO - ✅ Message processed and response sent successfully
2025-11-10T07:14:51.243414663Z 2025-11-10 07:14:51 - INFO - ================================================================================
2025-11-10T07:14:51.243580667Z INFO: 173.252.107.9:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:14:52.211013562Z 2025-11-10 07:14:52 - INFO - ================================================================================
2025-11-10T07:14:52.211040733Z 2025-11-10 07:14:52 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:14:52.211140615Z 2025-11-10 07:14:52 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRDgyOTQ4OTNFOTUyMUQ0QTlEAA==', 'status': 'sent', 'timestamp': '1762758891', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:52.211237747Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRDgyOTQ4OTNFOTUyMUQ0QTlEAA==', 'status': 'sent', 'timestamp': '1762758891', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:52.211241767Z 2025-11-10 07:14:52 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:14:52.211422301Z INFO: 173.252.127.5:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:14:53.471780389Z 2025-11-10 07:14:53 - INFO - ================================================================================
2025-11-10T07:14:53.471887322Z 2025-11-10 07:14:53 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:14:53.472033805Z 2025-11-10 07:14:53 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRDgyOTQ4OTNFOTUyMUQ0QTlEAA==', 'status': 'delivered', 'timestamp': '1762758892', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:53.472149387Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRDgyOTQ4OTNFOTUyMUQ0QTlEAA==', 'status': 'delivered', 'timestamp': '1762758892', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:53.472155587Z 2025-11-10 07:14:53 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:14:53.472372581Z INFO: 173.252.79.10:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:14:56.270774111Z 2025-11-10 07:14:56 - INFO - ================================================================================
2025-11-10T07:14:56.270819202Z 2025-11-10 07:14:56 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:14:56.270912784Z 2025-11-10 07:14:56 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRDgyOTQ4OTNFOTUyMUQ0QTlEAA==', 'status': 'read', 'timestamp': '1762758894', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:56.271048306Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRDgyOTQ4OTNFOTUyMUQ0QTlEAA==', 'status': 'read', 'timestamp': '1762758894', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:14:56.271059067Z 2025-11-10 07:14:56 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:14:56.271202969Z INFO: 173.252.79.32:0 - "POST /webhook HTTP/1.1" 200 OK
