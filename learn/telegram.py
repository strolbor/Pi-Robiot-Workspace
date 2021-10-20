import requests as req

# curl -X POST https://api.telegram.org/bot123456:abcde1234ABCDE/getUpdates

print(req.get('https://api.telegram.org/bot1233498807:AAGpVIwJMwxTvzcaMJmEog1NmN7XZZYlTDk/getUpdates'))


#curl -s -X POST https://api.telegram.org/bot1233498807:AAGpVIwJMwxTvzcaMJmEog1NmN7XZZYlTDk/sendMessage -d chat_id= -d text="Hello World"
print(req.get('https://api.telegram.org/bot1233498807:AAGpVIwJMwxTvzcaMJmEog1NmN7XZZYlTDk/sendMessage?chat_id=978618750&text="Hello World"'))