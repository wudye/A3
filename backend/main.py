from fastapi import FastAPI
from quantam import quantam_test
from predict import predict_test
app = FastAPI()

quantam_test()
predict_test()
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
