# ✈️ FlightsAPI

Una API REST construida con **FastAPI** y **MongoDB** para gestionar vuelos y pasajeros.

---

## 🚀 Tecnologías usadas

* Python 3.9
* FastAPI
* MongoDB (con Motor)
* Docker & Docker Compose

---

## 📦 Instalación y ejecución local

1. Clona el repositorio:

```bash
git clone <url-del-repo>
cd FlightsAPI
```

2. Ejecuta con Docker:

```bash
docker compose up --build
```

3. Accede a la API desde:

```
http://localhost:8000/
```

---

## 🗂️ Endpoints disponibles

### 🔹 Root

* `GET /`

  * Mensaje de bienvenida.

---

### ✈️ Vuelos

#### `GET /api/flights`

* Obtiene todos los vuelos registrados.

#### `GET /api/flights/{flight_code}`

* Obtiene los datos de un vuelo específico.

#### `POST /api/flights`

* Crea un nuevo vuelo.
* 🧾 JSON esperado:

```json
{
  "flightCode": "LAN123",
  "passengers": [
    {
        "id": 139577,
        "name": "Martín Alvarez",
        "hasConnections": false,
        "age": 2,
        "flightCategory": "Gold",
        "reservationId": "8ZC5KYVK",
        "hasCheckedBaggage": false
    },
    {
        "id": 530874,
        "name": "Jorge Hernández",
        "hasConnections": false,
        "age": 16,
        "flightCategory": "Black",
        "reservationId": "O2DQ3SZS",
        "hasCheckedBaggage": false
    },
    {
        "id": 426098,
        "name": "Pedro Ruiz",
        "hasConnections": false,
        "age": 33,
        "flightCategory": "Black",
        "reservationId": "KSXXOALO",
        "hasCheckedBaggage": true
    }
  ]
}
```
*Nota: también se puede entregar la lista passengers vacía.

#### `PUT /api/flights/{flight_code}`

* Actualiza el código de vuelo.
* 🧾 JSON esperado:

```json
{
  "newFlightCode": "LAN999"
}
```

#### `DELETE /api/flights/{flight_code}`

* Elimina un vuelo específico.

#### `DELETE /api/flights`

* Elimina **todos los vuelos** (CUIDADO!!!!).

---

### 🧍‍♂️ Pasajeros

#### `POST /api/flights/{flight_code}/passengers`

* Agrega un pasajero a un vuelo.
* 🧾 JSON esperado:

```json
{
  "id": 1,
  "name": "Martín Alvarez",
  "hasConnections": false,
  "age": 30,
  "flightCategory": "Gold",
  "reservationId": "ABC123",
  "hasCheckedBaggage": true
}
```

#### `PUT /api/flights/{flight_code}/passengers/{reservation_id}`

* Actualiza datos parciales de un pasajero.
* 🧾 JSON esperado (puedes enviar solo los campos a modificar):

```json
{
  "age": 31
}
```

#### `DELETE /api/flights/{flight_code}/passengers/{reservation_id}`

* Elimina un pasajero del vuelo.

---

## 🛠️ Variables de entorno

* `MONGO_URI`: conexión a MongoDB. Por defecto: `mongodb://mongo:27017`

---

## 📄 Notas finales

* Los pasajeros están embebidos dentro de cada vuelo en la base de datos por la estructura entregada de **Flight**.

---

Made with ❤️ using FastAPI
