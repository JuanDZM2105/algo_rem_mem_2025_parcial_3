#!/usr/bin/env python

marcos_libres = [0x0, 0x1, 0x2]
reqs = [0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A]
segmentos = [('.text', 0x00, 0x1A),
             ('.data', 0x40, 0x28),
             ('.heap', 0x80, 0x1F),
             ('.stack', 0xC0, 0x22)]

def procesar(segmentos, reqs, marcos_libres):
    tam_pagina = 16
    memoria = {}
    fifo_queue = []
    results = []

    def direccion_valida(req):
        for nombre, base, limite in segmentos:
            if base <= req < base + limite:
                return True
        return False

    for req in reqs:
        if not direccion_valida(req):
            results.append((req, 0x1ff, 'Segmentation Fault'))
            break

        pagina = req // tam_pagina
        offset = req % tam_pagina

        if pagina in memoria:
            marco = memoria[pagina]
            accion = 'Marco ya estaba asignado'
        else:
            if len(marcos_libres) > 0:
                marco = marcos_libres.pop(0)
                accion = 'Marco libre asignado'
            else:
                pag_salida = fifo_queue.pop(0)
                marco = memoria.pop(pag_salida)
                accion = 'Marco asignado'

            memoria[pagina] = marco
            fifo_queue.append(pagina)

        direccion_fisica = marco * tam_pagina + offset
        results.append((req, direccion_fisica, accion))

    return results


def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Dirección Física: {result[1]:#0{4}x} Acción: {result[2]}")


if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)

