2025-11-10T06:42:06.74204535Z Using cached google_auth_httplib2-0.2.1-py3-none-any.whl (9.5 kB)
2025-11-10T06:42:06.743089723Z Using cached httplib2-0.31.0-py3-none-any.whl (91 kB)
2025-11-10T06:42:06.744208747Z Using cached pyparsing-3.2.5-py3-none-any.whl (113 kB)
2025-11-10T06:42:06.745360901Z Using cached uritemplate-4.2.0-py3-none-any.whl (11 kB)
2025-11-10T06:42:06.746458505Z Using cached tqdm-4.67.1-py3-none-any.whl (78 kB)
2025-11-10T06:42:07.003379312Z Installing collected packages: pytz, websockets, uvloop, urllib3, uritemplate, tzlocal, typing-extensions, tqdm, sniffio, six, regex, pyyaml, pytokens, python-multipart, python-dotenv, pyparsing, pygments, pyflakes, pycodestyle, pyasn1, protobuf, pluggy, platformdirs, pathspec, packaging, mypy-extensions, mccabe, iniconfig, idna, httptools, h11, greenlet, dnspython, click, charset_normalizer, certifi, cachetools, annotated-types, annotated-doc, uvicorn, typing-inspection, rsa, requests, python-dateutil, pytest, pyee, pydantic-core, pyasn1-modules, proto-plus, mypy, httplib2, httpcore, gunicorn, grpcio, googleapis-common-protos, flake8, email-validator, black, anyio, watchfiles, starlette, pytest-asyncio, pydantic, playwright, httpx, grpcio-status, google-search-results, google-auth, dateparser, pydantic-settings, google-auth-httplib2, google-api-core, fastapi, google-api-python-client, google-ai-generativelanguage, google-generativeai
2025-11-10T06:42:36.159584557Z
2025-11-10T06:42:36.168467987Z Successfully installed annotated-doc-0.0.3 annotated-types-0.7.0 anyio-4.11.0 black-25.11.0 cachetools-6.2.1 certifi-2025.10.5 charset_normalizer-3.4.4 click-8.3.0 dateparser-1.2.2 dnspython-2.8.0 email-validator-2.3.0 fastapi-0.121.1 flake8-7.3.0 google-ai-generativelanguage-0.6.15 google-api-core-2.28.1 google-api-python-client-2.187.0 google-auth-2.43.0 google-auth-httplib2-0.2.1 google-generativeai-0.8.5 google-search-results-2.4.2 googleapis-common-protos-1.72.0 greenlet-3.2.4 grpcio-1.76.0 grpcio-status-1.71.2 gunicorn-23.0.0 h11-0.16.0 httpcore-1.0.9 httplib2-0.31.0 httptools-0.7.1 httpx-0.28.1 idna-3.11 iniconfig-2.3.0 mccabe-0.7.0 mypy-1.18.2 mypy-extensions-1.1.0 packaging-25.0 pathspec-0.12.1 platformdirs-4.5.0 playwright-1.55.0 pluggy-1.6.0 proto-plus-1.26.1 protobuf-5.29.5 pyasn1-0.6.1 pyasn1-modules-0.4.2 pycodestyle-2.14.0 pydantic-2.12.4 pydantic-core-2.41.5 pydantic-settings-2.11.0 pyee-13.0.0 pyflakes-3.4.0 pygments-2.19.2 pyparsing-3.2.5 pytest-8.4.2 pytest-asyncio-1.2.0 python-dateutil-2.9.0.post0 python-dotenv-1.2.1 python-multipart-0.0.20 pytokens-0.3.0 pytz-2025.2 pyyaml-6.0.3 regex-2025.11.3 requests-2.32.5 rsa-4.9.1 six-1.17.0 sniffio-1.3.1 starlette-0.49.3 tqdm-4.67.1 typing-extensions-4.15.0 typing-inspection-0.4.2 tzlocal-5.3.1 uritemplate-4.2.0 urllib3-2.5.0 uvicorn-0.38.0 uvloop-0.22.1 watchfiles-1.1.1 websockets-15.0.1
2025-11-10T06:42:36.17608809Z
2025-11-10T06:42:36.176102161Z [notice] A new release of pip is available: 25.1.1 -> 25.3
2025-11-10T06:42:36.176104941Z [notice] To update, run: pip install --upgrade pip
2025-11-10T06:42:46.783639904Z ==> Uploading build...
2025-11-10T06:43:07.301307163Z ==> Uploaded in 12.9s. Compression took 7.6s
2025-11-10T06:43:07.422291327Z ==> Build successful 🎉
2025-11-10T06:43:12.966784801Z ==> Deploying...
2025-11-10T06:43:53.698647211Z ==> Running 'uvicorn app.main:app --host 0.0.0.0 --port $PORT'
2025-11-10T06:44:09.482504327Z INFO: Started server process [58]
2025-11-10T06:44:09.482562329Z INFO: Waiting for application startup.
2025-11-10T06:44:09.482905206Z 2025-11-10 06:44:09 - INFO - 🚀 Starting Evara application...
2025-11-10T06:44:09.483044509Z 2025-11-10 06:44:09 - INFO - Environment: prod
2025-11-10T06:44:09.483146782Z 2025-11-10 06:44:09 - INFO - Debug mode: False
2025-11-10T06:44:09.483222504Z 2025-11-10 06:44:09 - INFO - Port: 10000
2025-11-10T06:44:09.483318976Z 2025-11-10 06:44:09 - INFO - ✅ Rate limiter initialized (10 messages/minute per user)
2025-11-10T06:44:09.483998051Z 2025-11-10 06:44:09 - INFO - ✅ Memory store preloaded
2025-11-10T06:44:09.484144544Z 2025-11-10 06:44:09 - INFO - ✅ Meta WhatsApp client initialized
2025-11-10T06:44:09.484152994Z 2025-11-10 06:44:09 - INFO - ✅ Meta WhatsApp client initialized successfully
2025-11-10T06:44:09.484248416Z 2025-11-10 06:44:09 - INFO - Phone Number ID: 822578864279365
2025-11-10T06:44:09.484698757Z 2025-11-10 06:44:09 - INFO - BeautifulSoup not installed - will use Playwright only
2025-11-10T06:44:09.484881511Z 2025-11-10 06:44:09 - INFO - ✅ Gemini model initialized successfully with gemini-2.0-flash
2025-11-10T06:44:09.484976983Z 2025-11-10 06:44:09 - INFO - ✅ Agent orchestrator initialized successfully
2025-11-10T06:44:09.485030954Z 2025-11-10 06:44:09 - INFO - ✅ Gemini client cached and ready
2025-11-10T06:44:09.485185468Z 2025-11-10 06:44:09 - INFO - ✅ Reminder checker started
2025-11-10T06:44:09.485247449Z 2025-11-10 06:44:09 - INFO - ✅ Memory cleanup scheduler started (runs every 24 hours)
2025-11-10T06:44:09.485327431Z 2025-11-10 06:44:09 - INFO - ✅ Evara is ready to receive messages! (Startup: 0.00s)
2025-11-10T06:44:09.485476814Z 2025-11-10 06:44:09 - INFO - ✅ Startup time 0.00s meets Render requirement (<60s)
2025-11-10T06:44:09.485708249Z 2025-11-10 06:44:09 - INFO - 🔄 Reminder checker loop started (checking every 15 seconds for accuracy)
2025-11-10T06:44:09.485829182Z 2025-11-10 06:44:09 - INFO - 🧹 Memory cleanup loop started (cleaning every 24 hours)
2025-11-10T06:44:09.485915724Z INFO: Application startup complete.
2025-11-10T06:44:09.583198763Z INFO: Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
2025-11-10T06:44:10.560524339Z INFO: 127.0.0.1:54030 - "HEAD / HTTP/1.1" 405 Method Not Allowed
2025-11-10T06:44:14.014820552Z ==> Your service is live 🎉
2025-11-10T06:44:14.231021226Z ==>
2025-11-10T06:44:14.422461802Z ==> ///////////////////////////////////////////////////////////
2025-11-10T06:44:15.036624508Z ==>
2025-11-10T06:44:15.229244854Z ==> Available at your primary URL https://evara-8w6h.onrender.com
2025-11-10T06:44:15.42245487Z ==>
2025-11-10T06:44:15.650852363Z ==> ///////////////////////////////////////////////////////////
2025-11-10T06:44:17.785859734Z INFO: 35.197.118.178:0 - "GET / HTTP/1.1" 200 OK
2025-11-10T06:44:24.486443348Z 2025-11-10 06:44:24 - INFO - ⏰ Reminder check at 12:14:24 PM IST - Found 0 pending reminder(s)
2025-11-10T06:44:39.487116783Z 2025-11-10 06:44:39 - INFO - ⏰ Reminder check at 12:14:39 PM IST - Found 0 pending reminder(s)
2025-11-10T06:44:54.487776686Z 2025-11-10 06:44:54 - INFO - ⏰ Reminder check at 12:14:54 PM IST - Found 0 pending reminder(s)
2025-11-10T06:45:03.948365574Z 2025-11-10 06:45:03 - INFO - ================================================================================
2025-11-10T06:45:03.948803973Z 2025-11-10 06:45:03 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T06:45:03.949129541Z 2025-11-10 06:45:03 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0IwNzQyOUNGRDAzMDFBNUMyMTUA', 'timestamp': '1762757102', 'text': {'body': 'set reminder for 12:16PM today IST time. topic “testing”'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T06:45:03.949308685Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0IwNzQyOUNGRDAzMDFBNUMyMTUA', 'timestamp': '1762757102', 'text': {'body': 'set reminder for 12:16PM today IST time. topic “testing”'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T06:45:03.949314775Z 2025-11-10 06:45:03 - INFO - From: whatsapp:917092724850
2025-11-10T06:45:03.949318155Z 2025-11-10 06:45:03 - INFO - Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0IwNzQyOUNGRDAzMDFBNUMyMTUA
2025-11-10T06:45:03.949484019Z 2025-11-10 06:45:03 - INFO - Body: set reminder for 12:16PM today IST time. topic “testing”...
2025-11-10T06:45:03.949789106Z 2025-11-10 06:45:03 - INFO - 🤖 Processing message from whatsapp:917092724850: set reminder for 12:16PM today IST time. topic “testing”...
2025-11-10T06:45:05.897229294Z 2025-11-10 06:45:05 - INFO - 📊 Intent: reminder (confidence: 0.95)
2025-11-10T06:45:05.897364507Z 2025-11-10 06:45:05 - INFO - 🔧 Executing tool for intent: reminder
2025-11-10T06:45:05.897595502Z 2025-11-10 06:45:05 - INFO - ⏰ Reminder requested: testing at 12:16PM today IST time (country: India, location: None)
2025-11-10T06:45:24.962367476Z 2025-11-10 06:45:24 - INFO - Created daily backup: /opt/render/project/src/taskflow/data/backups/user_memory_2025-11-10.json
2025-11-10T06:45:24.962387016Z 2025-11-10 06:45:24 - INFO - ✅ Generated response: Okay! I've set a reminder for you:
2025-11-10T06:45:24.962407277Z
2025-11-10T06:45:24.962414407Z 🗓️ November 10, 2025 at 12:16 PM (India)
2025-11-10T06:45:24.962420187Z 🔔 Topic: testing
2025-11-10T06:45:24.962424107Z
2025-11-10T06:45:24.962428108Z You n...
2025-11-10T06:45:24.962432468Z 2025-11-10 06:45:24 - INFO - 📤 Sending message via Meta WhatsApp to whatsapp:917092724850
2025-11-10T06:45:24.962437368Z 2025-11-10 06:45:24 - INFO - 📤 Sending Meta WhatsApp message to 917092724850
2025-11-10T06:45:25.792088659Z 2025-11-10 06:45:25 - INFO - ⏰ Reminder check at 12:15:25 PM IST - Found 0 pending reminder(s)
2025-11-10T06:45:26.631852469Z 2025-11-10 06:45:26 - INFO - ✅ Message sent successfully. Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSOEQ2NEQ0MTM0OTg5ODQ4Mjc1AA==
2025-11-10T06:45:26.631874749Z 2025-11-10 06:45:26 - INFO - ✅ Message processed and response sent successfully
2025-11-10T06:45:26.631880369Z 2025-11-10 06:45:26 - INFO - ================================================================================
2025-11-10T06:45:26.631885329Z INFO: 173.252.107.3:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T06:45:28.427297586Z 2025-11-10 06:45:28 - INFO - ================================================================================
2025-11-10T06:45:28.427388848Z 2025-11-10 06:45:28 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T06:45:28.427824148Z 2025-11-10 06:45:28 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSOEQ2NEQ0MTM0OTg5ODQ4Mjc1AA==', 'status': 'delivered', 'timestamp': '1762757127', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:45:28.427837648Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSOEQ2NEQ0MTM0OTg5ODQ4Mjc1AA==', 'status': 'delivered', 'timestamp': '1762757127', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:45:28.427854628Z 2025-11-10 06:45:28 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T06:45:28.42790905Z INFO: 173.252.107.112:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T06:45:28.83495699Z 2025-11-10 06:45:28 - INFO - ================================================================================
2025-11-10T06:45:28.835064723Z 2025-11-10 06:45:28 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T06:45:28.835153455Z 2025-11-10 06:45:28 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSOEQ2NEQ0MTM0OTg5ODQ4Mjc1AA==', 'status': 'sent', 'timestamp': '1762757127', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:45:28.835295508Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSOEQ2NEQ0MTM0OTg5ODQ4Mjc1AA==', 'status': 'sent', 'timestamp': '1762757127', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:45:28.835303278Z 2025-11-10 06:45:28 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T06:45:28.835533974Z INFO: 173.252.107.1:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T06:45:28.972315452Z 2025-11-10 06:45:28 - INFO - ================================================================================
2025-11-10T06:45:28.972430964Z 2025-11-10 06:45:28 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T06:45:28.974226545Z 2025-11-10 06:45:28 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSOEQ2NEQ0MTM0OTg5ODQ4Mjc1AA==', 'status': 'read', 'timestamp': '1762757127', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:45:28.974330287Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSOEQ2NEQ0MTM0OTg5ODQ4Mjc1AA==', 'status': 'read', 'timestamp': '1762757127', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:45:28.974335997Z 2025-11-10 06:45:28 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T06:45:28.974701226Z INFO: 173.252.79.4:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T06:45:40.792478479Z 2025-11-10 06:45:40 - INFO - ⏰ Reminder check at 12:15:40 PM IST - Found 0 pending reminder(s)
2025-11-10T06:45:55.803248701Z 2025-11-10 06:45:55 - INFO - ⏰ Reminder check at 12:15:55 PM IST - Found 0 pending reminder(s)
2025-11-10T06:46:09.030215825Z INFO: 136.233.9.100:0 - "GET /debug/reminders HTTP/1.1" 200 OK
2025-11-10T06:46:09.175909544Z INFO: 136.233.9.100:0 - "GET /favicon.ico HTTP/1.1" 404 Not Found
2025-11-10T06:46:10.803229507Z 2025-11-10 06:46:10 - INFO - ⏰ Reminder check at 12:16:10 PM IST - Found 0 pending reminder(s)
2025-11-10T06:46:25.803492968Z 2025-11-10 06:46:25 - INFO - ⏰ Reminder check at 12:16:25 PM IST - Found 0 pending reminder(s)
2025-11-10T06:46:40.804522874Z 2025-11-10 06:46:40 - INFO - ⏰ Reminder check at 12:16:40 PM IST - Found 0 pending reminder(s)
2025-11-10T06:46:55.805384974Z 2025-11-10 06:46:55 - INFO - ⏰ Reminder check at 12:16:55 PM IST - Found 0 pending reminder(s)
2025-11-10T06:47:10.805865403Z 2025-11-10 06:47:10 - INFO - ⏰ Reminder check at 12:17:10 PM IST - Found 0 pending reminder(s)
2025-11-10T06:47:25.806184281Z 2025-11-10 06:47:25 - INFO - ⏰ Reminder check at 12:17:25 PM IST - Found 0 pending reminder(s)
2025-11-10T06:47:33.77266983Z 2025-11-10 06:47:33 - INFO - ================================================================================
2025-11-10T06:47:33.772701361Z 2025-11-10 06:47:33 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T06:47:33.772830213Z 2025-11-10 06:47:33 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JDNzg3QThCQUE1OTcyMDRGRUUA', 'timestamp': '1762757252', 'text': {'body': 'did i asked you to set reminder?'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T06:47:33.772975407Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JDNzg3QThCQUE1OTcyMDRGRUUA', 'timestamp': '1762757252', 'text': {'body': 'did i asked you to set reminder?'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T06:47:33.772984897Z 2025-11-10 06:47:33 - INFO - From: whatsapp:917092724850
2025-11-10T06:47:33.773027208Z 2025-11-10 06:47:33 - INFO - Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JDNzg3QThCQUE1OTcyMDRGRUUA
2025-11-10T06:47:33.773150151Z 2025-11-10 06:47:33 - INFO - Body: did i asked you to set reminder?...
2025-11-10T06:47:33.773298344Z 2025-11-10 06:47:33 - INFO - 🤖 Processing message from whatsapp:917092724850: did i asked you to set reminder?...
2025-11-10T06:47:35.517209257Z 2025-11-10 06:47:35 - INFO - 📊 Intent: reminder (confidence: 0.90)
2025-11-10T06:47:35.517249608Z 2025-11-10 06:47:35 - INFO - 🔧 Executing tool for intent: reminder
2025-11-10T06:47:35.519680333Z 2025-11-10 06:47:35 - ERROR - Error executing tool: 'NoneType' object has no attribute 'lower'
2025-11-10T06:47:35.519694623Z Traceback (most recent call last):
2025-11-10T06:47:35.519700643Z File "/opt/render/project/src/taskflow/app/agent.py", line 484, in \_execute_tool
2025-11-10T06:47:35.519706273Z action = entities.get("reminder_action", "").lower()
2025-11-10T06:47:35.519712153Z ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-11-10T06:47:35.519717443Z AttributeError: 'NoneType' object has no attribute 'lower'
2025-11-10T06:47:36.809977758Z 2025-11-10 06:47:36 - INFO - ✅ Generated response: Yes, you did! 😊 I set a reminder for you on November 10, 2025 at 12:16 PM IST with the topic "testin...
2025-11-10T06:47:36.810009358Z 2025-11-10 06:47:36 - INFO - 📤 Sending message via Meta WhatsApp to whatsapp:917092724850
2025-11-10T06:47:36.810109371Z 2025-11-10 06:47:36 - INFO - 📤 Sending Meta WhatsApp message to 917092724850
2025-11-10T06:47:37.581818046Z 2025-11-10 06:47:37 - INFO - ✅ Message sent successfully. Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMDRGMzk3OUNENTBDODZGRTg4AA==
2025-11-10T06:47:37.582096383Z 2025-11-10 06:47:37 - INFO - ✅ Message processed and response sent successfully
2025-11-10T06:47:37.582113693Z 2025-11-10 06:47:37 - INFO - ================================================================================
2025-11-10T06:47:37.582315948Z INFO: 173.252.107.1:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T06:47:38.555284672Z 2025-11-10 06:47:38 - INFO - ================================================================================
2025-11-10T06:47:38.555315223Z 2025-11-10 06:47:38 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T06:47:38.555451736Z 2025-11-10 06:47:38 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMDRGMzk3OUNENTBDODZGRTg4AA==', 'status': 'sent', 'timestamp': '1762757257', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:47:38.556201623Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMDRGMzk3OUNENTBDODZGRTg4AA==', 'status': 'sent', 'timestamp': '1762757257', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:47:38.556210783Z 2025-11-10 06:47:38 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T06:47:38.556214233Z INFO: 173.252.127.113:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T06:47:39.41555863Z 2025-11-10 06:47:39 - INFO - ================================================================================
2025-11-10T06:47:39.415959139Z 2025-11-10 06:47:39 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T06:47:39.41596868Z 2025-11-10 06:47:39 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMDRGMzk3OUNENTBDODZGRTg4AA==', 'status': 'delivered', 'timestamp': '1762757258', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:47:39.415973Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMDRGMzk3OUNENTBDODZGRTg4AA==', 'status': 'delivered', 'timestamp': '1762757258', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:47:39.41599227Z 2025-11-10 06:47:39 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T06:47:39.416106243Z INFO: 173.252.79.10:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T06:47:40.806090811Z 2025-11-10 06:47:40 - INFO - ⏰ Reminder check at 12:17:40 PM IST - Found 0 pending reminder(s)
2025-11-10T06:47:43.946852197Z 2025-11-10 06:47:43 - INFO - ================================================================================
2025-11-10T06:47:43.94697169Z 2025-11-10 06:47:43 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T06:47:43.947105583Z 2025-11-10 06:47:43 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMDRGMzk3OUNENTBDODZGRTg4AA==', 'status': 'read', 'timestamp': '1762757263', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:47:43.947234516Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMDRGMzk3OUNENTBDODZGRTg4AA==', 'status': 'read', 'timestamp': '1762757263', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:47:43.947242646Z 2025-11-10 06:47:43 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T06:47:43.947479331Z INFO: 173.252.127.7:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T06:47:55.806667224Z 2025-11-10 06:47:55 - INFO - ⏰ Reminder check at 12:17:55 PM IST - Found 0 pending reminder(s)
2025-11-10T06:48:00.388817644Z 2025-11-10 06:48:00 - INFO - ================================================================================
2025-11-10T06:48:00.388859105Z 2025-11-10 06:48:00 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T06:48:00.388961048Z 2025-11-10 06:48:00 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JBNTAxMDhERjFENzMwNDZGMDkA', 'timestamp': '1762757279', 'text': {'body': 'what is my name again?'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T06:48:00.389030099Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'contacts': [{'profile': {'name': 'Rahul Yadav'}, 'wa_id': '917092724850'}], 'messages': [{'from': '917092724850', 'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JBNTAxMDhERjFENzMwNDZGMDkA', 'timestamp': '1762757279', 'text': {'body': 'what is my name again?'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
2025-11-10T06:48:00.389036969Z 2025-11-10 06:48:00 - INFO - From: whatsapp:917092724850
2025-11-10T06:48:00.389096041Z 2025-11-10 06:48:00 - INFO - Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAEhgUM0JBNTAxMDhERjFENzMwNDZGMDkA
2025-11-10T06:48:00.389156172Z 2025-11-10 06:48:00 - INFO - Body: what is my name again?...
2025-11-10T06:48:00.389232894Z 2025-11-10 06:48:00 - INFO - 🤖 Processing message from whatsapp:917092724850: what is my name again?...
2025-11-10T06:48:01.565755309Z 2025-11-10 06:48:01 - INFO - 📊 Intent: general (confidence: 0.90)
2025-11-10T06:48:02.552124385Z 2025-11-10 06:48:02 - INFO - ✅ Generated response: I don't have access to your personal information, so I don't know your name. 😊...
2025-11-10T06:48:02.552285348Z 2025-11-10 06:48:02 - INFO - 📤 Sending message via Meta WhatsApp to whatsapp:917092724850
2025-11-10T06:48:02.554089969Z 2025-11-10 06:48:02 - INFO - 📤 Sending Meta WhatsApp message to 917092724850
2025-11-10T06:48:03.206320086Z 2025-11-10 06:48:03 - INFO - ✅ Message sent successfully. Message ID: wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMUNBNTk5NEJFMzU4MDgzQzREAA==
2025-11-10T06:48:03.206584992Z 2025-11-10 06:48:03 - INFO - ✅ Message processed and response sent successfully
2025-11-10T06:48:03.206660964Z 2025-11-10 06:48:03 - INFO - ================================================================================
2025-11-10T06:48:03.206899959Z INFO: 173.252.107.2:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T06:48:04.168415976Z 2025-11-10 06:48:04 - INFO - ================================================================================
2025-11-10T06:48:04.168445356Z 2025-11-10 06:48:04 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T06:48:04.168547589Z 2025-11-10 06:48:04 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMUNBNTk5NEJFMzU4MDgzQzREAA==', 'status': 'sent', 'timestamp': '1762757283', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:48:04.168683252Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMUNBNTk5NEJFMzU4MDgzQzREAA==', 'status': 'sent', 'timestamp': '1762757283', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:48:04.168689482Z 2025-11-10 06:48:04 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T06:48:04.168862236Z INFO: 173.252.79.32:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T06:48:04.920820837Z 2025-11-10 06:48:04 - INFO - ================================================================================
2025-11-10T06:48:04.920851867Z 2025-11-10 06:48:04 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T06:48:04.92096663Z 2025-11-10 06:48:04 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMUNBNTk5NEJFMzU4MDgzQzREAA==', 'status': 'read', 'timestamp': '1762757284', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:48:04.921010801Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMUNBNTk5NEJFMzU4MDgzQzREAA==', 'status': 'read', 'timestamp': '1762757284', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:48:04.921034311Z 2025-11-10 06:48:04 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T06:48:04.921204665Z INFO: 173.252.107.6:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T06:48:05.14182121Z 2025-11-10 06:48:05 - INFO - ================================================================================
2025-11-10T06:48:05.141876691Z 2025-11-10 06:48:05 - INFO - 📨 Incoming Meta WhatsApp message
2025-11-10T06:48:05.141944483Z 2025-11-10 06:48:05 - INFO - Raw JSON payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMUNBNTk5NEJFMzU4MDgzQzREAA==', 'status': 'delivered', 'timestamp': '1762757284', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:48:05.142064535Z Incoming webhook payload: {'object': 'whatsapp_business_account', 'entry': [{'id': '812212521594090', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551505771', 'phone_number_id': '822578864279365'}, 'statuses': [{'id': 'wamid.HBgMOTE3MDkyNzI0ODUwFQIAERgSMUNBNTk5NEJFMzU4MDgzQzREAA==', 'status': 'delivered', 'timestamp': '1762757284', 'recipient_id': '917092724850', 'pricing': {'billable': False, 'pricing_model': 'PMP', 'category': 'service', 'type': 'free_customer_service'}}]}, 'field': 'messages'}]}]}
2025-11-10T06:48:05.142071956Z 2025-11-10 06:48:05 - WARNING - ⚠️ Could not parse Meta webhook message
2025-11-10T06:48:05.14226298Z INFO: 173.252.107.5:0 - "POST /webhook HTTP/1.1" 200 OK
2025-11-10T06:48:10.807804389Z 2025-11-10 06:48:10 - INFO - ⏰ Reminder check at 12:18:10 PM IST - Found 0 pending reminder(s)
