"""
RPC → REST Evolution — Protocol Stack Simulation (Apart_05-07).

Simulates three protocol eras for the same logical call:
  Era 1 — Raw RPC (Sun RPC / CORBA style): binary encoding, procedure IDs
  Era 2 — SOAP/XML Web Services: verbose XML envelope, WSDL-described
  Era 3 — REST/JSON: clean URL, lightweight JSON body

Each invocation returns the protocol representation + timing + byte size.
Shows WHY SOAP lost: the XML overhead is enormous vs the actual payload.
"""
import json
import time
from datetime import datetime


# ── Simulated Northwind data ──────────────────────────────────────────────────

_ORDERS = {
    10248: {'customer': 'Alfreds Futterkiste',  'country': 'Germany', 'total': 440.0},
    10249: {'customer': 'Toms Spezialitäten',   'country': 'Germany', 'total': 1863.4},
    10250: {'customer': 'Hanari Carnes',         'country': 'Brazil',  'total': 1552.6},
    10251: {'customer': 'Victuailles en stock',  'country': 'France',  'total': 654.06},
    10252: {'customer': 'Suprêmes délices',      'country': 'Belgium', 'total': 3597.9},
}


def _get_order_data(order_id: int) -> dict:
    return _ORDERS.get(order_id, {'customer': 'Unknown', 'country': '?', 'total': 0.0})


# ── Protocol generators ───────────────────────────────────────────────────────

def _rpc_representation(fn_id: int, order_id: int, result: dict) -> dict:
    """Simulated binary RPC encoding (XDR-like, as used in Sun RPC / CORBA)."""
    # XDR: 4 bytes per int/enum, null-padded strings to 4-byte boundaries
    customer_padded = result['customer'].ljust(((len(result['customer'])//4)+1)*4, '\x00')
    payload_hex = (
        f"00000001"                              # program number (1=Northwind)
        f"00000001"                              # version number
        f"{fn_id:08x}"                           # procedure ID
        f"{order_id:08x}"                        # arg: OrderID
        f"{''.join(f'{ord(c):02x}' for c in customer_padded[:20])}"
        f"{int(result['total']*100):08x}"        # total in cents
    )
    steps = [
        {'label': 'Client stub',     'detail': f'pack(fn={fn_id}, OrderID={order_id})'},
        {'label': 'Marshal (XDR)',   'detail': 'Convert args → binary XDR format'},
        {'label': 'TCP socket',      'detail': f'send({len(payload_hex)//2} bytes) → port 111'},
        {'label': 'Unmarshal',       'detail': 'Decode XDR bytes → server params'},
        {'label': 'Server skeleton', 'detail': f'invoke getOrder({order_id})'},
        {'label': 'Return marshal',  'detail': 'Encode result → XDR → TCP → client'},
    ]
    return {
        'protocol': 'RPC (XDR/binary)',
        'payload_hex': payload_hex[:120] + '…',
        'size_bytes': len(payload_hex) // 2,
        'steps': steps,
        'verdict': 'Fast, compact — but tightly coupled. Breaks across company boundaries. Language-specific.',
    }


def _soap_representation(order_id: int, result: dict) -> dict:
    """Simulated SOAP/XML Web Service envelope."""
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
  xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:nw="http://northwind.example.com/orders/wsdl">
  <soap:Header>
    <nw:AuthToken>Bearer eyJhbGciOiJSUzI1NiJ9…</nw:AuthToken>
    <nw:TransactionID>txn-{order_id}-{int(time.time())}</nw:TransactionID>
  </soap:Header>
  <soap:Body>
    <nw:GetOrderResponse>
      <nw:Order>
        <nw:OrderID xsi:type="xsd:integer">{order_id}</nw:OrderID>
        <nw:Customer xsi:type="xsd:string">{result['customer']}</nw:Customer>
        <nw:ShipCountry xsi:type="xsd:string">{result['country']}</nw:ShipCountry>
        <nw:OrderTotal xsi:type="xsd:decimal">{result['total']}</nw:OrderTotal>
        <nw:Status xsi:type="xsd:string">Shipped</nw:Status>
      </nw:Order>
    </nw:GetOrderResponse>
  </soap:Body>
</soap:Envelope>"""
    steps = [
        {'label': 'Client proxy',   'detail': 'Generated from WSDL (1400-line XML schema)'},
        {'label': 'SOAP encoder',   'detail': 'Wrap payload in Envelope/Header/Body XML'},
        {'label': 'HTTP POST',      'detail': f'POST /OrderService → {len(xml)} bytes'},
        {'label': 'XML parser',     'detail': 'Parse envelope, validate schema, XSD check'},
        {'label': 'Business logic', 'detail': f'getOrder({order_id}) → DB query'},
        {'label': 'SOAP response',  'detail': 'Wrap result in GetOrderResponse envelope'},
    ]
    return {
        'protocol': 'SOAP/XML (WS-* stack)',
        'payload': xml,
        'size_bytes': len(xml.encode('utf-8')),
        'steps': steps,
        'verdict': 'Interoperable, discoverable — but enormous overhead. A 40-byte answer wrapped in 800 bytes of XML.',
    }


def _rest_representation(order_id: int, result: dict) -> dict:
    """Simulated REST/JSON API call."""
    response = {
        'order_id':    order_id,
        'customer':    result['customer'],
        'ship_country': result['country'],
        'total':       result['total'],
        'status':      'shipped',
    }
    body = json.dumps(response, indent=2)
    steps = [
        {'label': 'HTTP GET',      'detail': f'GET /api/orders/{order_id}'},
        {'label': 'Route match',   'detail': 'URL pattern → handler function'},
        {'label': 'DB query',      'detail': f'SELECT … WHERE OrderID={order_id}'},
        {'label': 'JSON encode',   'detail': f'Serialize → {len(body)} bytes'},
        {'label': '200 OK',        'detail': 'Content-Type: application/json'},
    ]
    return {
        'protocol': 'REST/JSON (HTTP)',
        'payload': body,
        'url': f'GET /api/orders/{order_id}',
        'size_bytes': len(body.encode('utf-8')),
        'steps': steps,
        'verdict': 'Simple, cacheable, human-readable. Client needs no generated stub — any HTTP library works.',
    }


# ── Public API ────────────────────────────────────────────────────────────────

def rpc_invoke(order_id: int) -> dict:
    """Return all three protocol representations for the same logical request."""
    if order_id not in _ORDERS:
        order_id = 10248
    result = _get_order_data(order_id)

    t0 = time.perf_counter()
    rpc_rep  = _rpc_representation(fn_id=7, order_id=order_id, result=result)
    soap_rep = _soap_representation(order_id=order_id, result=result)
    rest_rep = _rest_representation(order_id=order_id, result=result)
    ms       = round((time.perf_counter() - t0) * 1000, 2)

    return {
        'order_id':  order_id,
        'order':     result,
        'protocols': {
            'rpc':  rpc_rep,
            'soap': soap_rep,
            'rest': rest_rep,
        },
        'size_comparison': {
            'rpc_bytes':  rpc_rep['size_bytes'],
            'soap_bytes': soap_rep['size_bytes'],
            'rest_bytes': rest_rep['size_bytes'],
        },
        'ts': datetime.now().strftime('%H:%M:%S'),
        'ms': ms,
    }


def rpc_get_orders() -> list:
    return [{'order_id': k, **v} for k, v in _ORDERS.items()]
