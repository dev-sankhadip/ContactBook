const userRouter=require('express').Router();
const shortId=require('shortid');
const { connection }=require('../db/db');

userRouter.post('/signup', function(request, response)
{
    const { name, email,password }=request.body;
    const userId=shortId.generate();
    const createUserQuery="insert into users(userid, username, email, password) values(?,?,?,?)";
    connection.query(createUserQuery,[userId, name, email, password], function(err, result)
    {
        if(err)
        {
            console.error(err)
            response.status(500).send({ code:500 })
        }
        response.status(200).send({ code:200 })
    })
})


userRouter.post('/login', function(request, response)
{
    const { email, password }=request.body;
    const loginUserQuery="select * from users where email = ?";
    connection.query(loginUserQuery,[email], function(err, result)
    {
        if(err)
        {
            response.status(500).send({ code:500 })
        }
        if(result.length>0)
        {
            if(result[0].password===password)
            {
                response.status(200).send({ code:200 })
            }
            else
            {
                response.status(401).send({ code:401 })
            }
        }
        else
        {
            response.status(400).send({ code:400 })
        }
    })
})

module.exports={
    userRouter
}