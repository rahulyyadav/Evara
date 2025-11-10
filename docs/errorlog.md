2025-11-10T07:18:20.222631471Z Using cached google_auth_httplib2-0.2.1-py3-none-any.whl (9.5 kB)
2025-11-10T07:18:20.224372904Z Using cached httplib2-0.31.0-py3-none-any.whl (91 kB)
2025-11-10T07:18:20.226119857Z Using cached pyparsing-3.2.5-py3-none-any.whl (113 kB)
2025-11-10T07:18:20.227917111Z Using cached uritemplate-4.2.0-py3-none-any.whl (11 kB)
2025-11-10T07:18:20.229573202Z Using cached tqdm-4.67.1-py3-none-any.whl (78 kB)
2025-11-10T07:18:20.507904715Z Installing collected packages: pytz, websockets, uvloop, urllib3, uritemplate, tzlocal, typing-extensions, tqdm, sniffio, six, regex, pyyaml, pytokens, python-multipart, python-dotenv, pyparsing, pygments, pyflakes, pycodestyle, pyasn1, protobuf, pluggy, platformdirs, pathspec, packaging, mypy-extensions, mccabe, iniconfig, idna, httptools, h11, greenlet, dnspython, click, charset_normalizer, certifi, cachetools, annotated-types, annotated-doc, uvicorn, typing-inspection, rsa, requests, python-dateutil, pytest, pyee, pydantic-core, pyasn1-modules, proto-plus, mypy, httplib2, httpcore, gunicorn, grpcio, googleapis-common-protos, flake8, email-validator, black, anyio, watchfiles, starlette, pytest-asyncio, pydantic, playwright, httpx, grpcio-status, google-search-results, google-auth, dateparser, pydantic-settings, google-auth-httplib2, google-api-core, fastapi, google-api-python-client, google-ai-generativelanguage, google-generativeai
2025-11-10T07:18:33.848464889Z
2025-11-10T07:18:33.857903Z Successfully installed annotated-doc-0.0.3 annotated-types-0.7.0 anyio-4.11.0 black-25.11.0 cachetools-6.2.1 certifi-2025.10.5 charset_normalizer-3.4.4 click-8.3.0 dateparser-1.2.2 dnspython-2.8.0 email-validator-2.3.0 fastapi-0.121.1 flake8-7.3.0 google-ai-generativelanguage-0.6.15 google-api-core-2.28.1 google-api-python-client-2.187.0 google-auth-2.43.0 google-auth-httplib2-0.2.1 google-generativeai-0.8.5 google-search-results-2.4.2 googleapis-common-protos-1.72.0 greenlet-3.2.4 grpcio-1.76.0 grpcio-status-1.71.2 gunicorn-23.0.0 h11-0.16.0 httpcore-1.0.9 httplib2-0.31.0 httptools-0.7.1 httpx-0.28.1 idna-3.11 iniconfig-2.3.0 mccabe-0.7.0 mypy-1.18.2 mypy-extensions-1.1.0 packaging-25.0 pathspec-0.12.1 platformdirs-4.5.0 playwright-1.55.0 pluggy-1.6.0 proto-plus-1.26.1 protobuf-5.29.5 pyasn1-0.6.1 pyasn1-modules-0.4.2 pycodestyle-2.14.0 pydantic-2.12.4 pydantic-core-2.41.5 pydantic-settings-2.11.0 pyee-13.0.0 pyflakes-3.4.0 pygments-2.19.2 pyparsing-3.2.5 pytest-8.4.2 pytest-asyncio-1.2.0 python-dateutil-2.9.0.post0 python-dotenv-1.2.1 python-multipart-0.0.20 pytokens-0.3.0 pytz-2025.2 pyyaml-6.0.3 regex-2025.11.3 requests-2.32.5 rsa-4.9.1 six-1.17.0 sniffio-1.3.1 starlette-0.49.3 tqdm-4.67.1 typing-extensions-4.15.0 typing-inspection-0.4.2 tzlocal-5.3.1 uritemplate-4.2.0 urllib3-2.5.0 uvicorn-0.38.0 uvloop-0.22.1 watchfiles-1.1.1 websockets-15.0.1
2025-11-10T07:18:33.865324473Z
2025-11-10T07:18:33.865340493Z [notice] A new release of pip is available: 25.1.1 -> 25.3
2025-11-10T07:18:33.865343493Z [notice] To update, run: pip install --upgrade pip
2025-11-10T07:18:37.231971187Z ==> Uploading build...
2025-11-10T07:18:53.521554823Z ==> Uploaded in 11.8s. Compression took 4.5s
2025-11-10T07:18:53.666518116Z ==> Build successful 🎉
2025-11-10T07:19:30.182599344Z ==> Deploying...
2025-11-10T07:20:03.222827271Z ==> Running 'uvicorn app.main:app --host 0.0.0.0 --port $PORT'
2025-11-10T07:20:17.823115497Z INFO: Started server process [59]
2025-11-10T07:20:17.823148158Z INFO: Waiting for application startup.
2025-11-10T07:20:17.823418835Z 2025-11-10 07:20:17 - INFO - 🚀 Starting Evara application...
2025-11-10T07:20:17.823477406Z 2025-11-10 07:20:17 - INFO - Environment: prod
2025-11-10T07:20:17.823546738Z 2025-11-10 07:20:17 - INFO - Debug mode: False
2025-11-10T07:20:17.823666291Z 2025-11-10 07:20:17 - INFO - Port: 10000
2025-11-10T07:20:17.823756303Z 2025-11-10 07:20:17 - INFO - ✅ Rate limiter initialized (10 messages/minute per user)
2025-11-10T07:20:17.824223335Z 2025-11-10 07:20:17 - INFO - ✅ Memory store preloaded
2025-11-10T07:20:17.824349048Z 2025-11-10 07:20:17 - INFO - ✅ Meta WhatsApp client initialized
2025-11-10T07:20:17.824366668Z 2025-11-10 07:20:17 - INFO - ✅ Meta WhatsApp client initialized successfully
2025-11-10T07:20:17.824454371Z 2025-11-10 07:20:17 - INFO - Phone Number ID: 822578864279365
2025-11-10T07:20:17.825065556Z 2025-11-10 07:20:17 - INFO - BeautifulSoup not installed - will use Playwright only
2025-11-10T07:20:17.825073886Z 2025-11-10 07:20:17 - INFO - ✅ Gemini model initialized successfully with gemini-2.0-flash
2025-11-10T07:20:17.825095137Z 2025-11-10 07:20:17 - INFO - ✅ Agent orchestrator initialized successfully
2025-11-10T07:20:17.825104437Z 2025-11-10 07:20:17 - INFO - ✅ Gemini client cached and ready
2025-11-10T07:20:17.825416605Z 2025-11-10 07:20:17 - INFO - ✅ Reminder checker started
2025-11-10T07:20:17.825748683Z 2025-11-10 07:20:17 - INFO - ✅ Memory cleanup scheduler started (runs every 24 hours)
2025-11-10T07:20:17.825760593Z 2025-11-10 07:20:17 - INFO - ✅ Evara is ready to receive messages! (Startup: 0.00s)
2025-11-10T07:20:17.825765463Z 2025-11-10 07:20:17 - INFO - ✅ Startup time 0.00s meets Render requirement (<60s)
2025-11-10T07:20:17.825770574Z 2025-11-10 07:20:17 - INFO - 🔄 Reminder checker loop started (checking every 15 seconds for accuracy)
2025-11-10T07:20:17.825775104Z 2025-11-10 07:20:17 - INFO - 🧹 Memory cleanup loop started (cleaning every 24 hours)
2025-11-10T07:20:17.825837325Z INFO: Application startup complete.
2025-11-10T07:20:17.922186909Z INFO: Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
2025-11-10T07:20:18.220724459Z INFO: 127.0.0.1:40648 - "HEAD / HTTP/1.1" 405 Method Not Allowed
2025-11-10T07:20:21.346999008Z ==> Your service is live 🎉
2025-11-10T07:20:21.545842173Z ==>
2025-11-10T07:20:21.741989879Z ==> ///////////////////////////////////////////////////////////
2025-11-10T07:20:21.936750225Z ==>
2025-11-10T07:20:22.148005799Z ==> Available at your primary URL https://evara-8w6h.onrender.com
2025-11-10T07:20:22.350295124Z ==>
2025-11-10T07:20:22.54967206Z ==> ///////////////////////////////////////////////////////////
2025-11-10T07:20:25.456343335Z INFO: 35.227.183.65:0 - "GET / HTTP/1.1" 200 OK
2025-11-10T07:20:32.826971672Z 2025-11-10 07:20:32 - INFO - ⏰ Reminder check at 12:50:32 PM IST - Found 0 pending reminder(s)
2025-11-10T07:20:47.82737787Z 2025-11-10 07:20:47 - INFO - ⏰ Reminder check at 12:50:47 PM IST - Found 0 pending reminder(s)
2025-11-10T07:21:01.79108246Z 2025-11-10 07:21:01 - INFO - ================================================================================
2025-11-10T07:21:01.791136062Z 2025-11-10 07:21:01 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:21:01.791246324Z 2025-11-10 07:21:01 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JBODZDOTkwOEY2Q0ZDQjUwOTYA', 'timestamp': '1762759260', 'text': {'body': 'search flights from chennai to bangalore on Dec 15'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:01.791391788Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JBODZDOTkwOEY2Q0ZDQjUwOTYA', 'timestamp': '1762759260', 'text': {'body': 'search flights from chennai to bangalore on Dec 15'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:01.791428519Z 2025-11-10 07:21:01 - INFO - From: whatsapp:917092724850
2025-11-10T07:21:01.7914599Z 2025-11-10 07:21:01 - INFO - Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JBODZDOTkwOEY2Q0ZDQjUwOTYA
2025-11-10T07:21:01.791514611Z 2025-11-10 07:21:01 - INFO - Body: search flights from chennai to bangalore on Dec 15...
2025-11-10T07:21:01.791591473Z 2025-11-10 07:21:01 - INFO - 🤖 Processing message from whatsapp:917092724850: search flights from chennai to bangalore on Dec 15...
2025-11-10T07:21:03.480465647Z 2025-11-10 07:21:03 - INFO - 📊 Intent: flight_search (confidence: 0.95)
2025-11-10T07:21:03.480726523Z 2025-11-10 07:21:03 - INFO - 🔧 Executing tool for intent: flight_search
2025-11-10T07:21:03.480893717Z 2025-11-10 07:21:03 - INFO - 🔍 Flight search entities - Origin: chennai, Destination: bangalore, Date: Dec 15
2025-11-10T07:21:03.481032661Z 2025-11-10 07:21:03 - INFO - ✈️ Flight search: chennai -> bangalore on Dec 15
2025-11-10T07:21:03.481488762Z 2025-11-10 07:21:03 - INFO - 📅 Parsing date: 'Dec 15'
2025-11-10T07:21:04.325654892Z 2025-11-10 07:21:04 - INFO - ✅ Parsed date: 'Dec 15' → 2025-12-15
2025-11-10T07:21:04.325823587Z 2025-11-10 07:21:04 - INFO - 🔍 Calling SerpAPI: chennai -> bangalore on 2025-12-15
2025-11-10T07:21:04.325901779Z 2025-11-10 07:21:04 - INFO - 🔄 Converting city names to airport codes...
2025-11-10T07:21:04.325979671Z 2025-11-10 07:21:04 - INFO - Origin: 'chennai'
2025-11-10T07:21:05.068586885Z 2025-11-10 07:21:05 - INFO - ✅ Converted 'chennai' to airport code: MAA
2025-11-10T07:21:05.068638066Z 2025-11-10 07:21:05 - INFO - Origin code: MAA
2025-11-10T07:21:05.068721619Z 2025-11-10 07:21:05 - INFO - Destination: 'bangalore'
2025-11-10T07:21:05.715973252Z 2025-11-10 07:21:05 - INFO - ✅ Converted 'bangalore' to airport code: BLR
2025-11-10T07:21:05.716088315Z 2025-11-10 07:21:05 - INFO - Destination code: BLR
2025-11-10T07:21:05.716098035Z 2025-11-10 07:21:05 - INFO - ✈️ SerpAPI Request: MAA -> BLR on 2025-12-15
2025-11-10T07:21:05.716168917Z 2025-11-10 07:21:05 - INFO - 📋 Full params: {'engine': 'google_flights', 'api_key': '123756fc070a2d2a5567893e7b213edbf2ab302d595bf0a48bfd9b12744ec23e', 'departure_id': 'MAA', 'arrival_id': 'BLR', 'outbound_date': '2025-12-15', 'type': '2', 'currency': 'INR', 'hl': 'en', 'gl': 'in'}
2025-11-10T07:21:06.126963915Z 2025-11-10 07:21:06 - INFO - 📡 Sending request to SerpAPI...
2025-11-10T07:21:06.220131132Z 2025-11-10 07:21:06 - INFO - ⏰ Reminder check at 12:51:06 PM IST - Found 0 pending reminder(s)
2025-11-10T07:21:07.562641799Z 2025-11-10 07:21:07 - INFO - 📡 SerpAPI Status Code: 200
2025-11-10T07:21:07.56270032Z 2025-11-10 07:21:07 - INFO - 📡 SerpAPI request URL: https://serpapi.com/search?engine=google_flights&api_key=123756fc070a2d2a5567893e7b213edbf2ab302d595bf0a48bfd9b12744ec23e&departure_id=MAA&arrival_id=BLR&outbound_date=2025-12-15&type=2&currency=INR&hl=en&gl=in
2025-11-10T07:21:07.562973867Z 2025-11-10 07:21:07 - INFO - 🔧 Formatting SerpAPI results...
2025-11-10T07:21:07.563056099Z 2025-11-10 07:21:07 - INFO - 📋 Response keys: ['search_metadata', 'search_parameters', 'best_flights', 'other_flights', 'price_insights', 'airports']
2025-11-10T07:21:07.563129351Z 2025-11-10 07:21:07 - INFO - ✅ Found 'best_flights' in response with 3 flights
2025-11-10T07:21:08.586669082Z 2025-11-10 07:21:08 - INFO - Created daily backup: /opt/render/project/src/taskflow/data/backups/user_memory_2025-11-10.json
2025-11-10T07:21:08.586688923Z 2025-11-10 07:21:08 - INFO - ✅ Generated response: Here are some flights from Chennai to Bangalore on December 15:
2025-11-10T07:21:08.586692703Z _ ₹2,849 (Direct)
2025-11-10T07:21:08.586695493Z _ ₹2,979 (Direct)
2025-11-10T07:21:08.586697873Z ...
2025-11-10T07:21:08.586714894Z 2025-11-10 07:21:08 - INFO - 📤 Sending message via Meta WhatsApp to whatsapp:917092724850
2025-11-10T07:21:08.586718194Z 2025-11-10 07:21:08 - INFO - 📤 Sending Meta WhatsApp message to 917092724850
2025-11-10T07:21:09.339259177Z 2025-11-10 07:21:09 - INFO - ✅ Message sent successfully. Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSQzc5NzhCQkFFMTUyREQwNjFDAA==
2025-11-10T07:21:09.339458913Z 2025-11-10 07:21:09 - INFO - ✅ Message processed and response sent successfully
2025-11-10T07:21:09.339516224Z 2025-11-10 07:21:09 - INFO - ================================================================================
2025-11-10T07:21:09.33974339Z INFO: 173.252.107.113:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:21:10.344330778Z 2025-11-10 07:21:10 - INFO - ================================================================================
2025-11-10T07:21:10.34438921Z 2025-11-10 07:21:10 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:21:10.344494033Z 2025-11-10 07:21:10 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSQzc5NzhCQkFFMTUyREQwNjFDAA==', 'status': 'sent', 'timestamp': '1762759269', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:10.344635056Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSQzc5NzhCQkFFMTUyREQwNjFDAA==', 'status': 'sent', 'timestamp': '1762759269', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:10.344641986Z 2025-11-10 07:21:10 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:21:10.344822771Z INFO: 173.252.107.2:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:21:11.513702343Z 2025-11-10 07:21:11 - INFO - ================================================================================
2025-11-10T07:21:11.513739584Z 2025-11-10 07:21:11 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:21:11.513838857Z 2025-11-10 07:21:11 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSQzc5NzhCQkFFMTUyREQwNjFDAA==', 'status': 'delivered', 'timestamp': '1762759270', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:11.513951569Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSQzc5NzhCQkFFMTUyREQwNjFDAA==', 'status': 'delivered', 'timestamp': '1762759270', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:11.51397425Z 2025-11-10 07:21:11 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:21:11.514140614Z INFO: 173.252.127.13:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:21:13.695551185Z 2025-11-10 07:21:13 - INFO - ================================================================================
2025-11-10T07:21:13.695674889Z 2025-11-10 07:21:13 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:21:13.695765261Z 2025-11-10 07:21:13 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSQzc5NzhCQkFFMTUyREQwNjFDAA==', 'status': 'read', 'timestamp': '1762759272', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:13.695907414Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSQzc5NzhCQkFFMTUyREQwNjFDAA==', 'status': 'read', 'timestamp': '1762759272', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:13.695920335Z 2025-11-10 07:21:13 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:21:13.696110119Z INFO: 173.252.79.48:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:21:21.220922728Z 2025-11-10 07:21:21 - INFO - ⏰ Reminder check at 12:51:21 PM IST - Found 0 pending reminder(s)
2025-11-10T07:21:30.071123619Z 2025-11-10 07:21:30 - INFO - ================================================================================
2025-11-10T07:21:30.071198681Z 2025-11-10 07:21:30 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:21:30.071281414Z 2025-11-10 07:21:30 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JGRjE4MTg0MkZERjBGQ0U0M0YA', 'timestamp': '1762759289', 'text': {'body': 'search flights from chennai to bagdogra on 2nd dec.'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:30.071401286Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JGRjE4MTg0MkZERjBGQ0U0M0YA', 'timestamp': '1762759289', 'text': {'body': 'search flights from chennai to bagdogra on 2nd dec.'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:30.071409337Z 2025-11-10 07:21:30 - INFO - From: whatsapp:917092724850
2025-11-10T07:21:30.071475218Z 2025-11-10 07:21:30 - INFO - Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JGRjE4MTg0MkZERjBGQ0U0M0YA
2025-11-10T07:21:30.0715339Z 2025-11-10 07:21:30 - INFO - Body: search flights from chennai to bagdogra on 2nd dec....
2025-11-10T07:21:30.071711954Z 2025-11-10 07:21:30 - INFO - 🤖 Processing message from whatsapp:917092724850: search flights from chennai to bagdogra on 2nd dec....
2025-11-10T07:21:32.242710541Z 2025-11-10 07:21:32 - INFO - 📊 Intent: flight_search (confidence: 0.95)
2025-11-10T07:21:32.242827364Z 2025-11-10 07:21:32 - INFO - 🔧 Executing tool for intent: flight_search
2025-11-10T07:21:32.242920297Z 2025-11-10 07:21:32 - INFO - 🔍 Flight search entities - Origin: chennai, Destination: bagdogra, Date: 2nd dec
2025-11-10T07:21:32.243023409Z 2025-11-10 07:21:32 - INFO - ✈️ Flight search: chennai -> bagdogra on 2nd dec
2025-11-10T07:21:32.243092201Z 2025-11-10 07:21:32 - INFO - 📅 Parsing date: '2nd dec'
2025-11-10T07:21:32.988104533Z 2025-11-10 07:21:32 - INFO - ✅ Parsed date: '2nd dec' → 2025-12-02
2025-11-10T07:21:32.988286388Z 2025-11-10 07:21:32 - INFO - 🔍 Calling SerpAPI: chennai -> bagdogra on 2025-12-02
2025-11-10T07:21:32.98834673Z 2025-11-10 07:21:32 - INFO - 🔄 Converting city names to airport codes...
2025-11-10T07:21:32.988397841Z 2025-11-10 07:21:32 - INFO - Origin: 'chennai'
2025-11-10T07:21:33.730161293Z 2025-11-10 07:21:33 - INFO - ✅ Converted 'chennai' to airport code: MAA
2025-11-10T07:21:33.730211364Z 2025-11-10 07:21:33 - INFO - Origin code: MAA
2025-11-10T07:21:33.730295436Z 2025-11-10 07:21:33 - INFO - Destination: 'bagdogra'
2025-11-10T07:21:34.378811198Z 2025-11-10 07:21:34 - INFO - ✅ Converted 'bagdogra' to airport code: IXB
2025-11-10T07:21:34.378837329Z 2025-11-10 07:21:34 - INFO - Destination code: IXB
2025-11-10T07:21:34.378931561Z 2025-11-10 07:21:34 - INFO - ✈️ SerpAPI Request: MAA -> IXB on 2025-12-02
2025-11-10T07:21:34.379004513Z 2025-11-10 07:21:34 - INFO - 📋 Full params: {'engine': 'google_flights', 'api_key': '123756fc070a2d2a5567893e7b213edbf2ab302d595bf0a48bfd9b12744ec23e', 'departure_id': 'MAA', 'arrival_id': 'IXB', 'outbound_date': '2025-12-02', 'type': '2', 'currency': 'INR', 'hl': 'en', 'gl': 'in'}
2025-11-10T07:21:34.429552196Z 2025-11-10 07:21:34 - INFO - 📡 Sending request to SerpAPI...
2025-11-10T07:21:35.629943387Z 2025-11-10 07:21:35 - INFO - 📡 SerpAPI Status Code: 200
2025-11-10T07:21:35.629977788Z 2025-11-10 07:21:35 - INFO - 📡 SerpAPI request URL: https://serpapi.com/search?engine=google_flights&api_key=123756fc070a2d2a5567893e7b213edbf2ab302d595bf0a48bfd9b12744ec23e&departure_id=MAA&arrival_id=IXB&outbound_date=2025-12-02&type=2&currency=INR&hl=en&gl=in
2025-11-10T07:21:35.630298416Z 2025-11-10 07:21:35 - INFO - 🔧 Formatting SerpAPI results...
2025-11-10T07:21:35.630371887Z 2025-11-10 07:21:35 - INFO - 📋 Response keys: ['search_metadata', 'search_parameters', 'best_flights', 'other_flights', 'price_insights', 'airports']
2025-11-10T07:21:35.630443219Z 2025-11-10 07:21:35 - INFO - ✅ Found 'best_flights' in response with 4 flights
2025-11-10T07:21:36.747464367Z 2025-11-10 07:21:36 - INFO - ✅ Generated response: Okay! Here are some flights from Chennai to Bagdogra on December 2nd:
2025-11-10T07:21:36.747496828Z _ ₹6,948 (Direct)
2025-11-10T07:21:36.747502838Z _ ₹7,260 (Di...
2025-11-10T07:21:36.747515179Z 2025-11-10 07:21:36 - INFO - 📤 Sending message via Meta WhatsApp to whatsapp:917092724850
2025-11-10T07:21:36.747679973Z 2025-11-10 07:21:36 - INFO - 📤 Sending Meta WhatsApp message to 917092724850
2025-11-10T07:21:36.919642929Z 2025-11-10 07:21:36 - INFO - ⏰ Reminder check at 12:51:36 PM IST - Found 0 pending reminder(s)
2025-11-10T07:21:37.570224394Z 2025-11-10 07:21:37 - INFO - ✅ Message sent successfully. Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNzIwREE0MTJCNDNEMjRDOUU1AA==
2025-11-10T07:21:37.570404378Z 2025-11-10 07:21:37 - INFO - ✅ Message processed and response sent successfully
2025-11-10T07:21:37.570439909Z 2025-11-10 07:21:37 - INFO - ================================================================================
2025-11-10T07:21:37.570652635Z INFO: 173.252.107.10:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:21:38.485668646Z 2025-11-10 07:21:38 - INFO - ================================================================================
2025-11-10T07:21:38.485688337Z 2025-11-10 07:21:38 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:21:38.485883322Z 2025-11-10 07:21:38 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNzIwREE0MTJCNDNEMjRDOUU1AA==', 'status': 'sent', 'timestamp': '1762759297', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:38.485962874Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNzIwREE0MTJCNDNEMjRDOUU1AA==', 'status': 'sent', 'timestamp': '1762759297', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:38.485971064Z 2025-11-10 07:21:38 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:21:38.486047656Z INFO: 173.252.79.34:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:21:39.263493541Z 2025-11-10 07:21:39 - INFO - ================================================================================
2025-11-10T07:21:39.263546442Z 2025-11-10 07:21:39 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:21:39.263666845Z 2025-11-10 07:21:39 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNzIwREE0MTJCNDNEMjRDOUU1AA==', 'status': 'delivered', 'timestamp': '1762759298', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:39.263780188Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNzIwREE0MTJCNDNEMjRDOUU1AA==', 'status': 'delivered', 'timestamp': '1762759298', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:39.263793438Z 2025-11-10 07:21:39 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:21:39.263948692Z INFO: 173.252.79.2:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:21:39.269175753Z 2025-11-10 07:21:39 - INFO - ================================================================================
2025-11-10T07:21:39.269188483Z 2025-11-10 07:21:39 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:21:39.269192763Z 2025-11-10 07:21:39 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNzIwREE0MTJCNDNEMjRDOUU1AA==', 'status': 'read', 'timestamp': '1762759298', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:39.269233524Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNzIwREE0MTJCNDNEMjRDOUU1AA==', 'status': 'read', 'timestamp': '1762759298', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:21:39.269241655Z 2025-11-10 07:21:39 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:21:39.269372538Z INFO: 173.252.107.5:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:21:51.919524042Z 2025-11-10 07:21:51 - INFO - ⏰ Reminder check at 12:51:51 PM IST - Found 0 pending reminder(s)
2025-11-10T07:22:06.920006845Z 2025-11-10 07:22:06 - INFO - ⏰ Reminder check at 12:52:06 PM IST - Found 0 pending reminder(s)
2025-11-10T07:22:07.751896419Z 2025-11-10 07:22:07 - INFO - ================================================================================
2025-11-10T07:22:07.75192465Z 2025-11-10 07:22:07 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:22:07.751998052Z 2025-11-10 07:22:07 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0IwNzhDMEQyODQ2NTBCOUNGNzEA', 'timestamp': '1762759326', 'text': {'body': 'great, thanks evara. \nI am Rahul 😊'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:07.752085954Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0IwNzhDMEQyODQ2NTBCOUNGNzEA', 'timestamp': '1762759326', 'text': {'body': 'great, thanks evara. \nI am Rahul 😊'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:07.752091714Z 2025-11-10 07:22:07 - INFO - From: whatsapp:917092724850
2025-11-10T07:22:07.752132535Z 2025-11-10 07:22:07 - INFO - Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0IwNzhDMEQyODQ2NTBCOUNGNzEA
2025-11-10T07:22:07.752200097Z 2025-11-10 07:22:07 - INFO - Body: great, thanks evara.
2025-11-10T07:22:07.752209487Z I am Rahul 😊...
2025-11-10T07:22:07.752286969Z 2025-11-10 07:22:07 - INFO - 🤖 Processing message from whatsapp:917092724850: great, thanks evara.
2025-11-10T07:22:07.752294649Z I am Rahul 😊...
2025-11-10T07:22:09.553833732Z 2025-11-10 07:22:09 - INFO - 📊 Intent: general (confidence: 0.90)
2025-11-10T07:22:10.406472626Z 2025-11-10 07:22:10 - INFO - ✅ Generated response: You're welcome, Rahul! 😊...
2025-11-10T07:22:10.406502197Z 2025-11-10 07:22:10 - INFO - 📤 Sending message via Meta WhatsApp to whatsapp:917092724850
2025-11-10T07:22:10.40661939Z 2025-11-10 07:22:10 - INFO - 📤 Sending Meta WhatsApp message to 917092724850
2025-11-10T07:22:11.234060794Z 2025-11-10 07:22:11 - INFO - ✅ Message sent successfully. Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNTkyQjFBQzA5ODg4QTBGMEJEAA==
2025-11-10T07:22:11.234489394Z 2025-11-10 07:22:11 - INFO - ✅ Message processed and response sent successfully
2025-11-10T07:22:11.234693399Z 2025-11-10 07:22:11 - INFO - ================================================================================
2025-11-10T07:22:11.235165921Z INFO: 173.252.127.39:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:22:12.312676587Z 2025-11-10 07:22:12 - INFO - ================================================================================
2025-11-10T07:22:12.312719988Z 2025-11-10 07:22:12 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:22:12.312830361Z 2025-11-10 07:22:12 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNTkyQjFBQzA5ODg4QTBGMEJEAA==', 'status': 'sent', 'timestamp': '1762759331', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:12.312941854Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNTkyQjFBQzA5ODg4QTBGMEJEAA==', 'status': 'sent', 'timestamp': '1762759331', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:12.312947384Z 2025-11-10 07:22:12 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:22:12.313124769Z INFO: 173.252.95.17:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:22:12.862295827Z 2025-11-10 07:22:12 - INFO - ================================================================================
2025-11-10T07:22:12.862333308Z 2025-11-10 07:22:12 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:22:12.862480371Z 2025-11-10 07:22:12 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNTkyQjFBQzA5ODg4QTBGMEJEAA==', 'status': 'delivered', 'timestamp': '1762759332', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:12.862581944Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNTkyQjFBQzA5ODg4QTBGMEJEAA==', 'status': 'delivered', 'timestamp': '1762759332', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:12.862587704Z 2025-11-10 07:22:12 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:22:12.862871501Z INFO: 173.252.95.14:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:22:12.940896962Z 2025-11-10 07:22:12 - INFO - ================================================================================
2025-11-10T07:22:12.940926683Z 2025-11-10 07:22:12 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:22:12.940970524Z 2025-11-10 07:22:12 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNTkyQjFBQzA5ODg4QTBGMEJEAA==', 'status': 'read', 'timestamp': '1762759332', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:12.941113657Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSNTkyQjFBQzA5ODg4QTBGMEJEAA==', 'status': 'read', 'timestamp': '1762759332', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:12.941118707Z 2025-11-10 07:22:12 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:22:12.941302442Z INFO: 173.252.95.40:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:22:21.920382632Z 2025-11-10 07:22:21 - INFO - ⏰ Reminder check at 12:52:21 PM IST - Found 0 pending reminder(s)
2025-11-10T07:22:36.921052141Z 2025-11-10 07:22:36 - INFO - ⏰ Reminder check at 12:52:36 PM IST - Found 0 pending reminder(s)
2025-11-10T07:22:38.317907583Z 2025-11-10 07:22:38 - INFO - ================================================================================
2025-11-10T07:22:38.317936894Z 2025-11-10 07:22:38 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:22:38.317991345Z 2025-11-10 07:22:38 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0I5ODQxQ0U4MkRFQkYzNjk3QjQA', 'timestamp': '1762759357', 'text': {'body': 'can you search the price of iphone 17 ?'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:38.318083398Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0I5ODQxQ0U4MkRFQkYzNjk3QjQA', 'timestamp': '1762759357', 'text': {'body': 'can you search the price of iphone 17 ?'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:38.318096888Z 2025-11-10 07:22:38 - INFO - From: whatsapp:917092724850
2025-11-10T07:22:38.318139759Z 2025-11-10 07:22:38 - INFO - Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0I5ODQxQ0U4MkRFQkYzNjk3QjQA
2025-11-10T07:22:38.318209181Z 2025-11-10 07:22:38 - INFO - Body: can you search the price of iphone 17 ?...
2025-11-10T07:22:38.318270342Z 2025-11-10 07:22:38 - INFO - 🤖 Processing message from whatsapp:917092724850: can you search the price of iphone 17 ?...
2025-11-10T07:22:40.063643161Z 2025-11-10 07:22:40 - INFO - 📊 Intent: price_track (confidence: 0.95)
2025-11-10T07:22:40.063708763Z 2025-11-10 07:22:40 - INFO - 🔧 Executing tool for intent: price_track
2025-11-10T07:22:40.063815196Z 2025-11-10 07:22:40 - INFO - 📦 Price tracking requested: iphone 17
2025-11-10T07:22:40.063884207Z 2025-11-10 07:22:40 - INFO - 🔍 Searching Google Shopping for: iphone 17
2025-11-10T07:22:42.878151541Z 2025-11-10 07:22:42 - ERROR - Error searching with SerpAPI: 'PriceTrackerTool' object has no attribute 'gemini_model'
2025-11-10T07:22:42.878175661Z Traceback (most recent call last):
2025-11-10T07:22:42.878180581Z File "/opt/render/project/src/taskflow/app/tools/price_tracker.py", line 462, in \_search_product_with_serpapi
2025-11-10T07:22:42.878185182Z if self.gemini_model and len(top_results) > 1:
2025-11-10T07:22:42.878189611Z ^^^^^^^^^^^^^^^^^
2025-11-10T07:22:42.878194852Z AttributeError: 'PriceTrackerTool' object has no attribute 'gemini_model'
2025-11-10T07:22:42.878274434Z 2025-11-10 07:22:42 - INFO - SerpAPI search failed, falling back to Amazon scraping
2025-11-10T07:22:46.027873937Z 2025-11-10 07:22:46 - ERROR - Error searching product: BrowserType.launch: Executable doesn't exist at /opt/render/.cache/ms-playwright/chromium_headless_shell-1187/chrome-linux/headless_shell
2025-11-10T07:22:46.027896827Z ╔════════════════════════════════════════════════════════════╗
2025-11-10T07:22:46.027902267Z ║ Looks like Playwright was just installed or updated. ║
2025-11-10T07:22:46.027906598Z ║ Please run the following command to download new browsers: ║
2025-11-10T07:22:46.027911748Z ║ ║
2025-11-10T07:22:46.027916248Z ║ playwright install ║
2025-11-10T07:22:46.027920238Z ║ ║
2025-11-10T07:22:46.027924328Z ║ <3 Playwright Team ║
2025-11-10T07:22:46.027928488Z ╚════════════════════════════════════════════════════════════╝
2025-11-10T07:22:46.027933668Z Traceback (most recent call last):
2025-11-10T07:22:46.027938338Z File "/opt/render/project/src/taskflow/app/tools/price_tracker.py", line 563, in \_search_and_get_product
2025-11-10T07:22:46.027942488Z browser = await self.\_ensure_browser()
2025-11-10T07:22:46.027946699Z ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-11-10T07:22:46.027951039Z File "/opt/render/project/src/taskflow/app/tools/price_tracker.py", line 81, in \_ensure_browser
2025-11-10T07:22:46.027955589Z self.browser = await self.\_playwright.chromium.launch(
2025-11-10T07:22:46.027959879Z ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-11-10T07:22:46.027964699Z ...<2 lines>...
2025-11-10T07:22:46.027968809Z )
2025-11-10T07:22:46.027973139Z ^
2025-11-10T07:22:46.027977819Z File "/opt/render/project/src/.venv/lib/python3.13/site-packages/playwright/async_api/\_generated.py", line 14465, in launch
2025-11-10T07:22:46.027982709Z await self.\_impl_obj.launch(
2025-11-10T07:22:46.027986709Z ...<17 lines>...
2025-11-10T07:22:46.02799082Z )
2025-11-10T07:22:46.0279956Z File "/opt/render/project/src/.venv/lib/python3.13/site-packages/playwright/\_impl/\_browser_type.py", line 98, in launch
2025-11-10T07:22:46.02799977Z await self.\_channel.send(
2025-11-10T07:22:46.02800401Z "launch", TimeoutSettings.launch_timeout, params
2025-11-10T07:22:46.02800833Z )
2025-11-10T07:22:46.02801249Z File "/opt/render/project/src/.venv/lib/python3.13/site-packages/playwright/\_impl/\_connection.py", line 69, in send
2025-11-10T07:22:46.02801646Z return await self.\_connection.wrap_api_call(
2025-11-10T07:22:46.028032021Z ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-11-10T07:22:46.028035101Z ...<3 lines>...
2025-11-10T07:22:46.028037701Z )
2025-11-10T07:22:46.028040181Z ^
2025-11-10T07:22:46.028042701Z File "/opt/render/project/src/.venv/lib/python3.13/site-packages/playwright/\_impl/\_connection.py", line 558, in wrap_api_call
2025-11-10T07:22:46.028045531Z raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
2025-11-10T07:22:46.028049041Z playwright.\_impl.\_errors.Error: BrowserType.launch: Executable doesn't exist at /opt/render/.cache/ms-playwright/chromium_headless_shell-1187/chrome-linux/headless_shell
2025-11-10T07:22:46.028051681Z ╔════════════════════════════════════════════════════════════╗
2025-11-10T07:22:46.028054201Z ║ Looks like Playwright was just installed or updated. ║
2025-11-10T07:22:46.028056731Z ║ Please run the following command to download new browsers: ║
2025-11-10T07:22:46.028059221Z ║ ║
2025-11-10T07:22:46.028061891Z ║ playwright install ║
2025-11-10T07:22:46.028064582Z ║ ║
2025-11-10T07:22:46.028067251Z ║ <3 Playwright Team ║
2025-11-10T07:22:46.028069902Z ╚════════════════════════════════════════════════════════════╝
2025-11-10T07:22:47.135382737Z 2025-11-10 07:22:47 - INFO - ✅ Generated response: I can't find the exact price for the iPhone 17 yet, as it hasn't been released.📱...
2025-11-10T07:22:47.135417088Z 2025-11-10 07:22:47 - INFO - 📤 Sending message via Meta WhatsApp to whatsapp:917092724850
2025-11-10T07:22:47.135532911Z 2025-11-10 07:22:47 - INFO - 📤 Sending Meta WhatsApp message to 917092724850
2025-11-10T07:22:47.885121759Z 2025-11-10 07:22:47 - INFO - ✅ Message sent successfully. Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRkYwMTMzMzkyQzZBRjIyMDREAA==
2025-11-10T07:22:47.885344205Z 2025-11-10 07:22:47 - INFO - ✅ Message processed and response sent successfully
2025-11-10T07:22:47.885430157Z 2025-11-10 07:22:47 - INFO - ================================================================================
2025-11-10T07:22:47.885714944Z INFO: 173.252.79.7:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:22:49.376243425Z 2025-11-10 07:22:49 - INFO - ================================================================================
2025-11-10T07:22:49.376341808Z 2025-11-10 07:22:49 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:22:49.37642413Z 2025-11-10 07:22:49 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRkYwMTMzMzkyQzZBRjIyMDREAA==', 'status': 'sent', 'timestamp': '1762759368', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:49.376521142Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRkYwMTMzMzkyQzZBRjIyMDREAA==', 'status': 'sent', 'timestamp': '1762759368', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:49.376544123Z 2025-11-10 07:22:49 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:22:49.376728587Z INFO: 173.252.95.20:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:22:49.936430287Z 2025-11-10 07:22:49 - INFO - ================================================================================
2025-11-10T07:22:49.93654961Z 2025-11-10 07:22:49 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:22:49.936678163Z 2025-11-10 07:22:49 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRkYwMTMzMzkyQzZBRjIyMDREAA==', 'status': 'delivered', 'timestamp': '1762759368', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:49.936801586Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRkYwMTMzMzkyQzZBRjIyMDREAA==', 'status': 'delivered', 'timestamp': '1762759368', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:49.936805806Z 2025-11-10 07:22:49 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:22:49.937009741Z INFO: 173.252.127.114:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T07:22:51.922034083Z 2025-11-10 07:22:51 - INFO - ⏰ Reminder check at 12:52:51 PM IST - Found 0 pending reminder(s)
2025-11-10T07:22:54.514540571Z 2025-11-10 07:22:54 - INFO - ================================================================================
2025-11-10T07:22:54.514576092Z 2025-11-10 07:22:54 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T07:22:54.514694125Z 2025-11-10 07:22:54 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRkYwMTMzMzkyQzZBRjIyMDREAA==', 'status': 'read', 'timestamp': '1762759373', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:54.514806687Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSRkYwMTMzMzkyQzZBRjIyMDREAA==', 'status': 'read', 'timestamp': '1762759373', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T07:22:54.514817558Z 2025-11-10 07:22:54 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T07:22:54.514954791Z INFO: 173.252.95.9:0 - "POST /webhook HTTP/1.1" 200 OK
