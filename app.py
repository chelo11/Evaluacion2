import os
import sys
from datetime import datetime

import requests


API_BASE_URL = os.getenv("API_BASE_URL", "https://mindicador.cl/api")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
PRESUPUESTO_CLP = int(os.getenv("PRESUPUESTO_CLP", "1500000"))
API_TOKEN_CHILE = os.getenv("API_TOKEN_CHILE", "")


def obtener_indicadores():
    try:
        headers = {}

        if API_TOKEN_CHILE:
            headers["Authorization"] = f"Bearer {API_TOKEN_CHILE}"

        respuesta = requests.get(
            API_BASE_URL,
            timeout=API_TIMEOUT,
            headers=headers
        )

        if respuesta.status_code in [401, 403]:
            raise PermissionError("Clave API invalida o sin permisos.")

        if respuesta.status_code == 404:
            raise FileNotFoundError("La ruta de la API no fue encontrada.")

        respuesta.raise_for_status()

        try:
            datos = respuesta.json()
        except ValueError:
            raise ValueError("La API no entrego una respuesta JSON valida.")

        campos_obligatorios = ["uf", "utm", "dolar", "euro"]

        for campo in campos_obligatorios:
            if campo not in datos:
                raise KeyError(f"Falta el campo obligatorio: {campo}")

            if "valor" not in datos[campo]:
                raise KeyError(f"El campo {campo} no contiene valor.")

        return datos

    except requests.exceptions.Timeout:
        print("ERROR: La API no respondio dentro del tiempo configurado.")
        sys.exit(1)

    except requests.exceptions.ConnectionError:
        print("ERROR: No fue posible conectarse con la API.")
        sys.exit(1)

    except PermissionError as error:
        print(f"ERROR DE CREDENCIAL: {error}")
        sys.exit(1)

    except FileNotFoundError as error:
        print(f"ERROR 404: {error}")
        sys.exit(1)

    except KeyError as error:
        print(f"ERROR DE DATOS: {error}")
        sys.exit(1)

    except ValueError as error:
        print(f"ERROR JSON: {error}")
        sys.exit(1)

    except requests.exceptions.RequestException as error:
        print(f"ERROR HTTP: {error}")
        sys.exit(1)


def mostrar_reporte(datos):
    fecha_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    uf = datos["uf"]["valor"]
    utm = datos["utm"]["valor"]
    dolar = datos["dolar"]["valor"]
    euro = datos["euro"]["valor"]

    presupuesto_en_uf = PRESUPUESTO_CLP / uf
    presupuesto_en_usd = PRESUPUESTO_CLP / dolar
    presupuesto_en_euro = PRESUPUESTO_CLP / euro

    print("REPORTE ECONOMICO PARA PYME CHILENA")
    print("-----------------------------------")
    print(f"Fecha de consulta: {fecha_consulta}")
    print(f"URL API utilizada: {API_BASE_URL}")
    print(f"Presupuesto configurado: ${PRESUPUESTO_CLP:,.0f} CLP")
    print("-----------------------------------")
    print(f"UF: ${uf:,.2f} CLP")
    print(f"UTM: ${utm:,.2f} CLP")
    print(f"Dolar observado: ${dolar:,.2f} CLP")
    print(f"Euro: ${euro:,.2f} CLP")
    print("-----------------------------------")
    print(f"Equivalente en UF: {presupuesto_en_uf:.2f} UF")
    print(f"Equivalente en USD: {presupuesto_en_usd:.2f} USD")
    print(f"Equivalente en EURO: {presupuesto_en_euro:.2f} EUR")
    print("-----------------------------------")
    print("Decision sugerida:")
    print("Revisar costos indexados a UF y compras internacionales antes de emitir cotizaciones.")


if __name__ == "__main__":
    indicadores = obtener_indicadores()
    mostrar_reporte(indicadores)
