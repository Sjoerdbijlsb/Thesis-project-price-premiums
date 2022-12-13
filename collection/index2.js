


const SneaksAPI = require('sneaks-api');
const sneaks = new SneaksAPI();
const fs = require('fs');

//C:\Users\sjoer\studies\Marketing analytics\courses\thesisMA\price-premiums-fashion\collection

const styleIDs = ["DZ6755-100", "FB8825-111", "387324-01", "bb650rwg", "cz8065-100", "dn2487-002", "u9060wcg", "u9060bcg", "bb650rwc",
"dv6994-001",  "m2002rup", "dx9999-600", "dz4865-503", "dc1974-005",  "DC1975-005/DM1054-005", "uxc72al", "uxc72au", "377586-01", "db2179-109", 
"CT8012-116", "378038-116", "DD1391-100", "DD1503-101", "cz8065-100", "HQ2153", "378040-116", "378039-116", "CW1590-100",
"DZ5485-612",  "1116109-CHE", "315122-111/CW2288-111"];



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
  }, index * 1000);
});



