const SneaksAPI = require('sneaks-api');
const sneaks = new SneaksAPI();
const fs = require('fs');


//Product object includes styleID where you input it in the getProductPrices function
//getProductPrices(styleID, callback) takes in a style ID and returns sneaker info including a price map and more images of the product
function getProductPrices(styleID) {
  sneaks.getProductPrices("FY2903", function(err, product){
    console.log(product);

    // check if the file exists, and creatcme an empty file if it doesn't
    if (!fs.existsSync('data.csv')) {
        fs.writeFileSync('data.csv', '');
    }

    // append the product data to the file
    fs.appendFile('data.csv', JSON.stringify(product), (err) => {
        if (err) throw err;
        console.log('Data saved to data.csv file!');
    });
  });
}

// call setInterval() to run the function every 5 seconds
setInterval(getProductPrices, 5000);

const interval = setInterval(getProductPrices, 5000);

// stop setInterval() from running after 10 seconds
setTimeout(() => {
  clearInterval(interval);
}, 10000);
