2025-11-10T05:20:28.249671107Z ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-11-10T05:20:28.249675328Z File "/opt/render/project/src/.venv/lib/python3.13/site-packages/click/core.py", line 814, in invoke
2025-11-10T05:20:28.249679798Z return callback(\*args, \*\*kwargs)
2025-11-10T05:20:28.249683788Z File "/opt/render/project/src/.venv/lib/python3.13/site-packages/uvicorn/main.py", line 423, in main
2025-11-10T05:20:28.249688409Z run(
2025-11-10T05:20:28.249692629Z ~~~^
2025-11-10T05:20:28.249696809Z app,
2025-11-10T05:20:28.249701069Z ^^^^
2025-11-10T05:20:28.249705919Z ...<46 lines>...
2025-11-10T05:20:28.24970928Z h11_max_incomplete_event_size=h11_max_incomplete_event_size,
2025-11-10T05:20:28.24971225Z ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-11-10T05:20:28.24971513Z )
2025-11-10T05:20:28.24971792Z ^
2025-11-10T05:20:28.249720851Z File "/opt/render/project/src/.venv/lib/python3.13/site-packages/uvicorn/main.py", line 593, in run
2025-11-10T05:20:28.249723701Z server.run()
2025-11-10T05:20:28.249726521Z ~~~~~~~~~~^^
2025-11-10T05:20:28.249730231Z File "/opt/render/project/src/.venv/lib/python3.13/site-packages/uvicorn/server.py", line 67, in run
2025-11-10T05:20:28.249734791Z return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
2025-11-10T05:20:28.249752953Z File "/opt/render/project/python/Python-3.13.4/lib/python3.13/asyncio/runners.py", line 195, in run
2025-11-10T05:20:28.249758093Z return runner.run(main)
2025-11-10T05:20:28.249762623Z ~~~~~~~~~~^^^^^^
2025-11-10T05:20:28.249767314Z File "/opt/render/project/python/Python-3.13.4/lib/python3.13/asyncio/runners.py", line 118, in run
2025-11-10T05:20:28.249771694Z return self.\_loop.run_until_complete(task)
2025-11-10T05:20:28.249776434Z ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
2025-11-10T05:20:28.249780744Z File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
2025-11-10T05:20:28.249785315Z File "/opt/render/project/src/.venv/lib/python3.13/site-packages/uvicorn/server.py", line 71, in serve
2025-11-10T05:20:28.249789725Z await self.\_serve(sockets)
2025-11-10T05:20:28.249793035Z File "/opt/render/project/src/.venv/lib/python3.13/site-packages/uvicorn/server.py", line 78, in \_serve
2025-11-10T05:20:28.249795845Z config.load()
2025-11-10T05:20:28.249798785Z ~~~~~~~~~~~^^
2025-11-10T05:20:28.249801656Z File "/opt/render/project/src/.venv/lib/python3.13/site-packages/uvicorn/config.py", line 439, in load
2025-11-10T05:20:28.249804556Z self.loaded_app = import_from_string(self.app)
2025-11-10T05:20:28.249815806Z ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
2025-11-10T05:20:28.249818167Z File "/opt/render/project/src/.venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
2025-11-10T05:20:28.249819947Z module = importlib.import_module(module_str)
2025-11-10T05:20:28.249830167Z File "/opt/render/project/python/Python-3.13.4/lib/python3.13/importlib/**init**.py", line 88, in import_module
2025-11-10T05:20:28.249832158Z return \_bootstrap.\_gcd_import(name[level:], package, level)
2025-11-10T05:20:28.249833868Z ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-11-10T05:20:28.249835578Z File "<frozen importlib._bootstrap>", line 1387, in \_gcd_import
2025-11-10T05:20:28.249837358Z File "<frozen importlib._bootstrap>", line 1360, in \_find_and_load
2025-11-10T05:20:28.249839398Z File "<frozen importlib._bootstrap>", line 1331, in \_find_and_load_unlocked
2025-11-10T05:20:28.249841158Z File "<frozen importlib._bootstrap>", line 935, in \_load_unlocked
2025-11-10T05:20:28.249842818Z File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-11-10T05:20:28.249844498Z File "<frozen importlib._bootstrap>", line 488, in \_call_with_frames_removed
2025-11-10T05:20:28.249846259Z File "/opt/render/project/src/taskflow/app/main.py", line 20, in <module>
2025-11-10T05:20:28.249847988Z from .agent import AgentOrchestrator
2025-11-10T05:20:28.249849669Z File "/opt/render/project/src/taskflow/app/agent.py", line 1021
2025-11-10T05:20:28.249851829Z """
2025-11-10T05:20:28.249854689Z ^
2025-11-10T05:20:28.249859189Z SyntaxError: unterminated triple-quoted string literal (detected at line 1043)
