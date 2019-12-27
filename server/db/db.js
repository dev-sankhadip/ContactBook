const mysql=require('mysql');
require('dotenv').config();

const connection=mysql.createPool({
    host:process.env.HOST,
    database:process.env.DATABASE,
    user:process.env.USER,
    password:process.env.PASSWORD
})

module.exports={
    connection
}