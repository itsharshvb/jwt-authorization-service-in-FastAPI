import uvicorn
from fastapi import FastAPI, Body, Depends
from model import PostSchema, UserSchema, UserLoginSchema
from auth.jwt_handler import signJWT
from auth.jwt_bearer import jwtBearer

posts = [
    {
        "id": 1,
        "title": "Penguins ",
        "text": "Penguins are a group of aquatic flightless birds."
    },
    {
        "id": 2,
        "title": "Tigers ",
        "text": "Tigers are the largest living cat species and a memeber of the genus panthera."
    },
    {
        "id": 3,
        "title": "Koalas ",
        "text": "Koala is arboreal herbivorous maruspial native to Australia."
    },
]

users = []

app = FastAPI()

# testing get


@app.get("/", tags=["test"])
def greet():
    return {"hello": "world!"}

# Get Post


@app.get("/posts", tags=["posts"])
def get_post():
    return {"data": posts}

# Get one post by id


@app.get("/posts/{id}", tags=["posts"])
def get_post_by_id(id: int):
    if id > len(posts):
        return {"error": "Post doesn't exist"}
    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }

# post a single post


@app.post("/posts", dependencies=[Depends(jwtBearer())], tags=["posts"])
def create_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.model_dump())
    return {
        "info": "post added"
    }

# user signup [Create a new User]


@app.post("/user/signup", tags=['user'])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)


def checkUser(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False


@app.post("/user/login", tags=['user'])
def user_login(user: UserLoginSchema = Body(default=None)):
    if checkUser(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login Details"
        }
