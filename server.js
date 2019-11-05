const fs = require('fs');
const server = require('http').createServer();
const Route = require('router');
const router = new Route();
const finalhandler = require('finalhandler');

server.on('request', function (request, response) {
    router(request, response, finalhandler(request, response));
});
server.listen(8000);

router.get('/', function(request, response) {
    response.writeHead(200, {'content-type': 'text/html'});
    fs.createReadStream('./index.html').pipe(response);
});