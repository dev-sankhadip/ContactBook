const express=require('express');
const logger=require('morgan');
const cors=require('cors');

const app=express();

// set middlewares
app.use(logger('dev'));
app.use(cors());
app.use(express.json())
app.use(express.urlencoded({ extended:true }))

// get all routes
const { userRouter }=require('./routes/user');

app.use('/cli', userRouter);



app.listen(2222,()=>
{
    console.log('listening on 2222');
})