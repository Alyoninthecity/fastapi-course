netstat -ano | findstr :8000

taskkill /PID `<PID>` /F

cd ./TodoApp/

uvicorn main:app --reload
