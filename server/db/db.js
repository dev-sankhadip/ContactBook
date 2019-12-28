const mysql=require('mysql');

const connection=mysql.createPool({
    host:'localhost',
    database:'contact',
    user:'root',
    password:'root'
})

module.exports={
    connection
}