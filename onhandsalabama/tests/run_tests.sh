docker rm -f "onhands-alabama"
docker run -i -t -v "$(pwd):/home/onhands-alabama/" -p 0.0.0.0:5432:5432 -p 0.0.0.0:8080:8080 --name "onhands-alabama" "onhands-alabama:latest" sh -c "./test.sh"
# docker run -i -t -v "$(pwd):/home/onhands-alabama/" -p 0.0.0.0:5432:5432 --name "onhands-alabama" "onhands-alabama:latest" sh -c "./test.sh"
