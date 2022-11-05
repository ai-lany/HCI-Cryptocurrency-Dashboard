const faker = require("faker");

const arr = []
for (let i = 1; i < 25; i++) {
    const address = faker.address.nearbyGPSCoordinate([25.755608, -80.371298], i*0.3, false);
    arr.push([address[0].toString(), address[1].toString()])
}

console.log(arr);
