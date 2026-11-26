def visible():
    return [{'in': {'queryIP': '172.16.254.1'}}, {'in': {'queryIP': '2001:0db8:85a3:0:0:8A2E:0370:7334'}}, {'in': {'queryIP': '256.256.256.256'}}]

def hidden():
    return [{'in': {'queryIP': ''}}, {'in': {'queryIP': '0.0.0.0'}}, {'in': {'queryIP': '01.01.01.01'}}, {'in': {'queryIP': '1.1.1.1.'}}, {'in': {'queryIP': '192.168.1.1a'}}, {'in': {'queryIP': '2001:0db8:85a3::8A2E:0370:7334'}}, {'in': {'queryIP': '2001:0db8:85a3:0000:0000:8a2e:0370:7334:'}}, {'in': {'queryIP': '2001:0db8:85a3:0:0:8A2E:0370:733g'}}, {'in': {'queryIP': 'ffff:FFFF:0:1:23:456:789a:BcDe'}}]
