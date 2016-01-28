docker rm -f "onhands-alabama"
docker run -i -t -v "$(pwd):/home/onhands-alabama/" --name "onhands-alabama" "onhands-alabama:latest" sh -c "sudo service postgresql start; onhands up --wsgifile app.py"
# docker run -i -t  -v "$(pwd):/home/alabama/" --name "alabama" "alabama:latest" /bin/bash
