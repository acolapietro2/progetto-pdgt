//Librerie
const express = require('express');
const request = require('request');
const where = require("lodash.where");
const app = express();

// Link da dove vengono presi i dati
const link_dati = "https://data.cityofnewyork.us/api/geospatial/a9we-mtpn?method=export&format=GeoJSON";

// I dati saranno contenuti qua
var data_store;

// Descrizione API
app.get('/', function (req, res) {
  var dsc = '';
  dsc = "Utilizzo:<br>";
  dsc += "* /hotspots => Ritorna tutti gli hotspot<br>";
  dsc += "* /hotspots/:city='nomedellacittà' => Ritorna solo gli hotspot nella città specificata<br>";
  res.send(dsc);
  // stato funzionamento server
  res.status(200);
});

// Richiesta base
app.get('/hotspots', function (req, res) {
  
  // Carico i dati esterni
  request(link_dati, function (error, response, body) {
    data_store = JSON.parse(body);
  });
  res.send(data_store);
  res.status(200);
});

// Richiesta con filtro
app.get('/hotspots/:city', function (req, res) {
  // Carico i dati esterni
  request(link_dati, function (error, response, body) {
    data_store = JSON.parse(body);
  });
  var filtered = data_store;
  // Filtro i dati
  filtered['features'] = where(data_store['features'], {"properties": {"city": req.params.city.replace(':city=','')}});

  res.send(filtered);  
  res.status(200);
});

const server = app.listen(process.env.PORT || 8000, function () {
  
});
