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
    console.log("[CALLBACK]");
    const params = req.query;
    console.log("[CALLBACK] Recibidos:", params);

    const jsonString = JSON.stringify(params, null, 2);
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

    const html = `
      <html>
        <head>
          <title>Resultado del Callback</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 20px; background: #f8f8f8; }
            pre { background: #eee; padding: 15px; border-radius: 5px; overflow-x: auto; }
            h2 { color: #333; }
          </style>
        </head>
        <body>
          <h1>✅ Callback recibido</h1>

          <h2>Petición entrante (params recibidos del SSO Fake)</h2>
          <pre>${jsonString}</pre>

          <h2>Petición saliente (programData base64)</h2>
          <pre>${base64Encoded}</pre>

          <h2>Respuesta de Rappi</h2>
          <pre>${JSON.stringify(response.data, null, 2)}</pre>
        </body>
      </html>
    `;

    res.send(html);

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
