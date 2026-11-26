# Kiro provider plugin notes

Plugin: `/opt/data/plugins/kiro-provider` (upstream `anpicasso/hermes-kiro-provider`, subdir `provider/`). Files: `__init__.py` (ProviderProfile: `supports_vision`, `default_aux_model`, `model_capabilities`), `client.py` (`KiroClient`, OpenAI-chat-shaped), `translate.py` (OpenAI messages → Kiro `conversationState`), `credentials.py` (pooled OAuth rows from `hermes auth add kiro`).

## Direct probe

```python
import sys; sys.path.insert(0, "/opt/data/plugins/kiro-provider")
from hermes_cli.env_loader import load_hermes_dotenv; load_hermes_dotenv()
from client import KiroClient, list_model_ids
from translate import build_request
c = KiroClient()
print(list_model_ids())  # live catalog
print(c._create(model="claude-haiku-5.5", messages=[{"role": "user", "content": "4-word title for: X"}]).choices[0].message.content)
```

## Images

- Kiro's runtime accepts images on the current user message: `body["conversationState"]["currentMessage"]["userInputMessage"]["images"] = [{"format": "png", "source": {"bytes": <base64>}}]`, sent via `c._complete(model, body)`. Works on a plain user turn and on a tool-result turn (`userInputMessageContext.toolResults` present).
- `translate._text()` keeps only `type == "text"` parts, so OpenAI `image_url` parts (data URLs) are silently dropped. A vision fix must extract `image_url` data URLs into the `images` list (format from the MIME type) for user and tool messages.
- Images also work in history `userInputMessage`s and in tool-result turns, so forward them everywhere, not only on the current message.
- Upstream plugin (v1.0.1) has no image support. The local patch (`translate._images` forwards base64 `image_url`/`input_image` parts for current, history and tool-result turns; `__init__` sets `supports_vision=True` and a per-model `_ModelCapabilities` dict subclass whose `.get()` answers any live catalog id) is saved as `/opt/data/patches/kiro-provider-vision.patch`. Re-apply after any plugin reinstall/update (`hermes plugins` update overwrites it).
- Declare per-model vision via `model_capabilities`, not just the profile flag: `_lookup_supports_vision` reads `model_capabilities` through models.dev overrides, while profile `supports_vision` only gates images inside tool results.
- Text-only on Kiro (400 "doesn't support the image content block"): deepseek, minimax, glm, qwen families. Claude and GPT-5.6 models accept images. Probe new models by sending one image to each id from `list_model_ids()`.
- Only base64 data URLs are forwarded; Hermes' vision tools already inline local/remote images before they reach the provider.

## Sync aux calls inside a running event loop

- Symptom: `Title generation failed: ... invalid response (type=coroutine): '<coroutine object to_thread ...>'`. `KiroClient._create` returned `asyncio.to_thread(...)` whenever a loop was running, but `title_generation` calls sync `call_llm` from a thread that has a loop, so the unawaited coroutine reached `_validate_llm_response`.
- Fix (local, plugin v1.0.1): `_create` returns a `_LazyResponse` (a `collections.abc.Coroutine` subclass, so `asyncio.create_task` accepts it) that runs the request inline on attribute access and in a worker thread on `await`. A plain `__await__`-only wrapper breaks the plugin's own `create_task` test. Upstream-ready branches and PR text: `/opt/data/patches/hermes-kiro-provider-prs/`; the test suite needs `PYTHONPATH=/opt/hermes:<hermes venv site-packages>` and `test_native_profile_declares_auth_catalog_and_capabilities` already fails on upstream `main` here. Patch: `/opt/data/patches/kiro-provider-sync-in-loop.patch`. Re-apply after plugin updates, like the vision patch. Verify with sync-no-loop, sync-in-loop and `async_call_llm` calls in a fresh venv process.

## Reasoning fields (`additionalModelRequestFields`)

- Symptom: `Title generation failed: Kiro runtime failed (400): Invalid additionalModelRequestFields: property 'enabled' is not defined in the schema`. Hermes passes its generic `reasoning_config` (`{"enabled": False}`, `{"effort": ...}`) as `extra_body.reasoning`, and plugin v1.0.1 forwarded it verbatim.
- Kiro's strict schema (probed): Claude takes `{"thinking": {"type": "adaptive"|"disabled"}, "output_config": {"effort": low|medium|high|xhigh|max}}`; GPT-5.6 takes `{"reasoning": {"effort": none|low|medium|high|xhigh|max}}`. `claude-opus-5.5` allows only `adaptive` (400 enumeration ["adaptive"]).
- Local fix: `client._kiro_reasoning_fields(model, cfg)` maps the generic config per family (native-shaped dicts pass through, `minimal`→low, `ultra`→max), and `_complete` retries a rejected `disabled` as adaptive + low effort. Patch: `/opt/data/patches/kiro-provider-reasoning-fields.patch` (diff vs `/opt/data/backups/kiro-provider-20261109T115032Z`). Re-apply after plugin updates.
- Tests: pytest is not in the Hermes venv; use `$TMPDIR/tv` (`python -m venv --system-site-packages` + `pip install pytest`).

## Credits

- `fetch_account_usage` returns one `Credit` window (`detail` like `358/1000`, monthly reset) plus an extra-usage detail line. It already feeds `/usage` and the model picker; see `references/interim-plugins.md` for why it is not visible elsewhere and how the interim `kiro-credits` plugin appends it to replies.
