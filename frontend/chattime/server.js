const express = require('express');
const path = require('path');
const app = express();

// Serve your HTML file
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'chattime.html'));
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Website running at http://localhost:${PORT}`);
});

// added this because I could not get my image to load from the views folder so the html file could display it
app.use(express.static('views'));

app.use(express.static(__dirname));