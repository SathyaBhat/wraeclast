# YNAB MCP — Direct HTTP/curl Access

Use when debugging or scripting outside Hermes tool calls.

## Server URL
```
https://wraeclast.bishop-bass.ts.net/ynab-mcp
```
Auth header: `Authorization: Bearer $MCP_YNAB_MCP_API_KEY`

## Step 1 — Initialize session (get Mcp-Session-Id)
```bash
curl -s -X POST "$URL" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -D - \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"hermes","version":"1.0"}}}'
# → response headers contain: mcp-session-id: XXXXXXXX
# → body (SSE): event: message\ndata: {"jsonrpc":"2.0","id":1,"result":{...}}
```

## Step 2 — Call a tool
```bash
SESSION_ID="<from step 1>"
curl -s -X POST "$URL" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"<TOOL_NAME>","arguments":{...}}}'
```

## Parsing SSE responses
```python
import json

with open('/tmp/ynab_response.txt') as f:
    content = f.read()

for line in content.split('\n'):
    if line.startswith('data: '):
        data = json.loads(line[6:])
        if 'result' in data:
            payload = json.loads(data['result']['content'][0]['text'])
            # payload is a list (transactions) or dict (month data, etc.)
            break
```

## Notes
- The session ID persists for the life of the shell session — initialize once, reuse.
- Responses are SSE (`text/event-stream`), not plain JSON. Always strip the `data: ` prefix.
- `result.content[0].text` is a JSON-encoded string — double-parse required.
