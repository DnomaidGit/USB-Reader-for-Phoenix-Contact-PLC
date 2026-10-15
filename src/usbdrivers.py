import struct
import sys

if len(sys.argv) != 2:
    print("Usage: python3 usbdrivers.py <EventNumber>")
    sys.exit(1)

event_num = sys.argv[1]
event_file = f'/dev/input/event{event_num}'

# Mapa de teclado español sin SHIFT
key_map = {
    2: '1', 3: '2', 4: '3', 5: '4', 6: '5',
    7: '6', 8: '7', 9: '8', 10: '9', 11: '0',
    12: "'", 13: '¡',
    16: 'Q', 17: 'W', 18: 'E', 19: 'R', 20: 'T',
    21: 'Y', 22: 'U', 23: 'I', 24: 'O', 25: 'P',
    26: '`', 27: '+',
    30: 'A', 31: 'S', 32: 'D', 33: 'F', 34: 'G',
    35: 'H', 36: 'J', 37: 'K', 38: 'L',
    39: 'Ñ', 40: '´', 41: 'Ç', 43: '<',
    44: 'Z', 45: 'X', 46: 'C', 47: 'V',
    48: 'B', 49: 'N', 50: 'M',
    51: ',', 52: '.', 53: '-', 57: ' '
}

# Caracteres especiales con SHIFT
shift_map = {
    2: '!', 3: '"', 4: '·', 5: '$', 6: '%',
    7: '&', 8: '/', 9: '(', 10: ')', 11: '=',
    12: '?', 13: '¿',
    26: '^', 27: '*',
    40: '¨', 41: 'ª', 43: '>',
    51: ';', 52: ':', 53: '_'
}

buffer = []
shift_pressed = False

# Formato de evento Linux de 64 bits
event_format = 'llHHI'
event_size = struct.calcsize(event_format)

with open(event_file, 'rb') as f:
    while True:
        event = f.read(event_size)

        if len(event) < event_size:
            break

        sec, usec, event_type, code, value = struct.unpack(
            event_format, event
        )

        # Solo eventos de teclado
        if event_type != 1:
            continue

        # SHIFT izquierdo (42) o derecho (54)
        if code in (42, 54):
            shift_pressed = value != 0
            continue

        # Procesar solo pulsaciones
        if value != 1:
            continue

        # ENTER: enviar código completo
        if code == 28:
            sys.stdout.write("".join(buffer) + "\n")
            sys.stdout.flush()
            buffer = []
            continue

        # Obtener carácter
        if shift_pressed and code in shift_map:
            char = shift_map[code]
        else:
            char = key_map.get(code, '')

            # Convertir letras a minúsculas sin SHIFT
            if char.isalpha() and not shift_pressed:
                char = char.lower()

        if char:
            buffer.append(char)

