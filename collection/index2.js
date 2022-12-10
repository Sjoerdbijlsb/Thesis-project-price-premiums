const SneaksAPI = require('sneaks-api');
const sneaks = new SneaksAPI();
const fs = require('fs');

const styleIDs = ["DZ6755-100", "F8825-111", "387324-01", "bb650rwg", "cz8065-100-lyf-book", "dn2487-002", "u9060wcg", "u9060bcg", "bb650rwc",
"dv6994-001",  "m2002rup", "dx9999-600", "dz4865-503", "dc1975-005", "uxc72al", "uxc72au", "hp9260", "377586-01", "db2179-109",
"377612-01"];

function getProductPrices(styleID) {
  sneaks.getProductPrices(styleID, function(err, product){
    console.log(product);

    // check if the file exists, and create an empty file if it doesn't
    fs.access('data.json', fs.constants.F_OK, function (err) {
      if (err) {
        fs.writeFileSync('data.json', '{ "data": [] }');
      }
    });

    try {
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
    } catch(err) {
      // log the error and continue with the next iteration
      console.error(err);
    }
  });
}
    



styleIDs.forEach((styleID, index) => {
  // use setTimeout() to wait 1 second before calling the getProductPrices() function
  setTimeout(() => {
    getProductPrices(styleID);
  }, index * 300);
});



