var util = require('util')
var sleep = require('sleep');
var express = require('express');
var cors = require('cors')
var chokidar = require('chokidar');
var fs = require('fs');
var app = express();
var SyncPromise = require('sync-promise');


app.use(cors())
app.all('/', function(req, res, next) {
  res.header("Access-Control-Allow-Origin", req.header.origin);
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  next();
 });
app.use(function(req, res, next) {  
  res.header('Access-Control-Allow-Origin', 'http://localhost:8081');
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
  res.header(
    'Access-Control-Allow-Headers', 'Content-Type, Authorization, Content-Length, X-Requested-With, X-Api-Key'
  );
  res.header('Access-Control-Allow-Credentials', 'true');
  if ('OPTIONS' === req.method) {
    res.sendStatus(200);
  }
  else {
    next();
  }
});


var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : 'mysql',
  database : 'krama_db'
});
    connection.connect();


var server = require('http').createServer(app);  
//var io = require('socket.io')(server,{origins:'http://localhost:8082'});
var socket = require('socket.io');
var io = socket.listen(server);

app.use('/public', express.static('public'));
app.use('/pages', express.static('pages'));


app.get('/index', function (req, res)
{
    res.render('/pages/index.html');
});

app.get('/data', function (req, res) {

   res.header('Access-Control-Allow-Origin', 'http://localhost:8081');
   res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
   res.header('Access-Control-Allow-Headers', 'Content-Type');
   res.send(get_graph_json());
})


app.get('/execdata', function (req, res) {
   get_execdata_json().then(function(rows){
    res.send(rows)
   })
})

function get_execdata_json(){
    return new SyncPromise(function(resolve,reject){
    connection.query('SELECT a.* FROM executions_tab a join (select distinct(exec_id) from executions_tab order by exec_id desc limit 5) b on a.exec_id=b.exec_id;', function(err, rows, fields)
    {
      if(err) reject('query error')
      resolve(rows);
    });
    })    
}

function get_graph_json() {
  var graph_json
  //graph_json=JSON.parse(execSync("python -m expresso.lib.main -print"));
  path=fs.readFileSync('refresh.txt').toString()
  path=path.replace(/(\r\n|\n|\r)/gm,"");
  console.log(path+'aaa')
  if(path==''){
    path='/home/jaley/Projects/project1/.executions/exec_89/main.json'
  }
  if(fs.existsSync(path)){
    graph_json=JSON.parse(fs.readFileSync(path).toString())
  }else{
    path='/home/jaley/Projects/project1/.executions/exec_89/main.json'
    graph_json=JSON.parse(fs.readFileSync(path).toString())
    console.log("GRAPH MADE")
    console.log(graph_json)
  }

  return graph_json
  // body...
}


io.on('connection', function(socket){
  console.log("Connected")
  chokidar.watch('./refresh.txt', {ignored: /[\/\\]\./}).on('all', (event, path) => {
  console.log(event, path);
  console.log("File Changed")
   //io.emit('chat message', JSON.stringify(get_graph_json()));
      get_execdata_json().then(function(rows)
      {
        io.emit('trigger',rows)
      })
  });
  });




server.listen(8082)
