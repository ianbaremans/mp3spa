docker stop mp3spa_kont
docker rm mp3spa_kont
docker rmi mp3spa:latest
docker build -t mp3spa .
docker run -d --name mp3spa_kont -p 80:80 mp3spa:latest
