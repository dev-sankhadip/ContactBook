const userRouter=require('express').Router();
const shortId=require('shortid');
const fileUpload=require('express-fileupload');
const { connection }=require('../db/db');


userRouter.use(fileUpload())

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

userRouter.post('/backup', function(request, response)
{
    console.log(request.files);
    const { userid, email, password }=request.body;

    const sql="select * from users where email = ?";
    connection.query(sql,[email], function(err, result)
    {
        if(err)
        {
            response.send({ code:500, message:"Internal Server error" })
            return;
        }
        if(result.length>0)
        {
            if(result.password===password)
            {
                const pathToBeSaved='/home/sankha/Desktop/contact-cli/server/user_backup_db_file/';
                if(request.files){
                    const filename=request.files.image.name;
                    request.files.image.mv(`${pathToBeSaved}${filename}`,(err)=>
                    {
                        if(err)
                        {
                            response.send({ code:500, message:"Internal error" });
                        }
                        response.send({ code:200,message:"File backedup" });
                    })
                }else{
                    response.send({ code:500 });
                }
            }
            else
            {
                response.send({ code:301, message:"Wrong password" });
            }
        }
        else
        {
            response.send({ code:400, message:"User not found" });
        }
    })
})

module.exports={
    userRouter
}