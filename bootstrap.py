import uvicorn


def run_server():
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    run_server()
