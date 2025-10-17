// server.js
const express = require('express');
const app = express();
const port = 4000;
const axios = require('axios');
const querystring = require('querystring');

//home
app.get('/', (req, res) => {
  res.send(`
    <h1>Servidor de Callback para Doters</h1>
    <p>Este servidor recibe el callback desde el SSO fake de Doters y reenvía los datos a Rappi.</p>
  `);
});

//callback
app.get('/callback', async (req, res) => {
  try {
    const params = req.query;
    console.log("[CALLBACK] Recibidos:", params);

    const jsonString = JSON.stringify(params);
    const base64Encoded = Buffer.from(jsonString).toString('base64');

    const body = {
      programData: base64Encoded
    };

    console.log("[CALLBACK] Enviando a Rappi:", body);

    const response = await axios.post(
      'http://127.0.0.1:8080/api/lifemiles-integration/internal-ms/miles-integration/authentication/191000068534',
      body,
      {
        headers: {
          'Content-Type': 'application/json',
          'miles-program': 'DOTERS'
        }
      }
    );

    res.send({
      status: 'success',
      data_sent: body,
      rappi_response: response.data
    });
  } catch (error) {
    console.error("[CALLBACK] Error:", error.message);
    res.status(500).send({
      status: 'error',
      message: error.message
    });
  }
});

app.listen(port, () => {
  console.log(`Callback server corriendo en http://127.0.0.1:${port}`);
});
