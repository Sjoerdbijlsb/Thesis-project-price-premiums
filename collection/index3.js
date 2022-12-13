const SneaksAPI = require('sneaks-api');
const sneaks = new SneaksAPI();
const fs = require('fs');

const styleIDs = ["z1891-401"];

function getProductPrices(styleID) {
  sneaks.getProductPrices(styleID, function(err, product){
    console.log(product);

    // check if the file exists, and create an empty file if it doesn't
    fs.access('data.json', fs.constants.F_OK, (err) => {
      if (err) {
        fs.writeFileSync('data.json', '{ "data": [] }');
      }
    });

    // read the file and parse the JSON
    fs.readFile('data.json', 'utf8', (err, fileData) => {
      if (err) throw err;
      let data = JSON.parse(fileData);

      // append the product data to the file
      data.data.push(product);

      // write the updated data to the file
      fs.writeFile('data.json', JSON.stringify(data), (err) => {
        if (err) throw err;
        console.log('Data saved to data.json file!');
      });
    });
  });
}

// call setInterval() to run the function every 5 seconds
const interval = setInterval(() => {
  // call the getProductPrices function for each style ID
  styleIDs.forEach(styleID => getProductPrices(styleID));
}, 5000);

// stop setInterval() from running after 10 seconds
setTimeout(() => {
  clearInterval(interval);
}, 10000);
