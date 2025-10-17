<h1 align="center"> FelipedelosH </h1>
<br>
<h4>Fake DOTERS PYTHON FLASK SERVER</h4>

![Banner](Docs/banner.png)
<br>
:construction: Active Development  
This repository simulates the **DOTERS loyalty API** using **Python + Flask**, designed as a *mock server* for integration testing between **Rappi** and **Doters** services. :construction:
<br><br>
FakeServerDOTERS is a modular Flask application that emulates the real behavior of the **Doters API**, allowing developers to test authentication, signup, points accrual, redemptions, and other loyalty program workflows **without connecting to production services**.

The server follows a **clean layered architecture**, using:
> `Controller → UseCase → Service → Repository → Database (SQLite)`


## :hammer:Funtions:

- `/health`: Check server status.<br>
- `/v1/security/login`: Validate user credentials and return mock auth token.<br>
- `Function X`: ABC.<br>


## Architecture

```
FakeServerDOTERS/
├─ app/
│  ├─ controllers/
│  │  └─ 
│  ├─ Database/
│  │  └─
│  ├─ helpers/
│  │  └─ 
│  ├─ models/
│  │  └─ 
│  ├─ repositories/
│  │  └─ 
│  ├─ services/
│  │  └─ 
│  │  UseCases/
│  │  └─ 
│  ├─ __init__.py
│  └─ routes.py
│
├─ DB/
├─ .gitignore
├─ readme.md
├─ requirements.txt
└─ run.py
```

## Install requirements.txt


```
C:\Users\docto\AppData\Local\Programs\Python\Python313\python.exe -m pip install -r requirements.txt
```
```
pip install -r requirements.txt
```

## :play_or_pause_button:How to execute a project

```
C:\Users\docto\AppData\Local\Programs\Python\Python313\python.exe run.py
```
```
python run.py
```

## Endpoints

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/` | GET | SEND params to reditect /LOGIN |
| `/login` | GET | Open Browser and login in APP |
| `/health` | GET | Check server status |
| `/v1/security/login` | POST | Generate authentication token |
| `/v1/security/generate-otp` | POST | Generate OTP for member |
| `/v1/security/validate-otp` | POST | Validate OTP for member |
| `/v1/member-transactions/points/accrual/delivery` | POST | Accrue points |
| `/v1/member-transactions/points/simulate/delivery` | POST | Simulate points accrual |
| `/v1/member-transactions/points/redemption/delivery` | POST | Redeem points |
| `/v1/member-transactions/points/redemption/simulate/delivery` | POST | Simulate redemption |
| `/v1/member-transactions/points/cancel-transaction` | POST | Cancel a transaction |
| `/v2/member-transactions/rates` | GET | Get exchange rate |
| `/v1/member-account/link/rappi` | POST | Link Rappi and Doters accounts |
| `/v1/member-account/unlink/rappi` | POST | Unlink Rappi and Doters accounts |
| `/v2/user/signup` | POST | Automatic user signup |


## :hammer_and_wrench:Tech.

- Python
- Flask
- SQLite3
- Layered architecture
- Postman

## :warning:Warning.

- Passwords are stored in plain text (mock-only).
- OTP and token generation are not secure (for simulation purposes only).
- Data persistence resets when the SQLite DB file is deleted.
- Not intended for production environments.

## Autor

| [<img src="https://avatars.githubusercontent.com/u/38327255?v=4" width=115><br><sub>Andrés Felipe Hernánez</sub>](https://github.com/felipedelosh)|
| :---: |