const userRouter=require('express').Router();
const { connection }=require('../db/db');

userRouter.post('/signup', function(request, response)
{
    console.log(request.body);
})

module.exports={
    userRouter
}