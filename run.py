import uvicorn

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="127.0.0.1", port=7091, reload=True)
    except KeyboardInterrupt:
        print("\n[INFO] Deteniendo el servidor...")
        
