import re

def extract_device_id(values):
    candidates = []

    for v in values:
        v = v.strip().upper()

        matches_alpha = re.finditer(r'(?<!\d)([A-Z]\d{6,7})(?!\d)', v)
        for m in matches_alpha:
            s = m.group(1)
            start_idx = m.start()
            if start_idx > 0 and v[start_idx-1].isalpha():
                prefix = v[:start_idx]
                allow = any(prefix.endswith(p) for p in ('SNO', 'NO', 'SLNO', 'SRNO', 'SL.NO', 'SR.', 'SL.', 'SR', 'L.NO', 'P.', 'C.'))
                if not allow:
                    continue
            candidates.append(s)

        matches_digit = re.finditer(r'(?<!\d)(\d{7,8})(?!\d)', v)
        for m in matches_digit:
            start_idx = m.start()
            if start_idx > 0 and v[start_idx-1].isalpha():
                prefix = v[:start_idx]
                allow = any(prefix.endswith(p) for p in ('SNO', 'NO', 'SLNO', 'SRNO', 'SL.NO', 'SR.', 'SL.', 'SR', 'L.NO', 'P.', 'C.'))
                if not allow:
                    continue
            candidates.append(m.group(1))

    if not candidates:
        return None

    # prefer UXXXXXXX format
    for c in candidates:
        if re.match(r'[A-Z]\d{6,7}', c):
            return c

    return candidates[0]

test_cases = [
    "NOVEMBER20251330F",
    "LAT12345678",
    "SNOU5979820",
    "U5979820",
    "860710080664447",
    "NO20278928",
    "U5006273"
]

for t in test_cases:
    print(f"{t} -> {extract_device_id([t])}")
