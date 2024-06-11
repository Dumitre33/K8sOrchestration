from app import app  # Import the initialized Quart application

@app.route('/')
async def hello():
    return 'Hello'

def main():
    app.run(host='127.0.0.1', port=5000)


if __name__ == '__main__':
    main() # Start the server


