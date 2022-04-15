const { readFileSync } = require('fs');
const { PinSeeker } = require('./dist/index');

(async () => {
    const file = readFileSync('map.png');
    const x = await PinSeeker.find(file);
    console.log(JSON.stringify(x,null,2));
})();