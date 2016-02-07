docker rm -f "onhands-alabama"

docker run -i -t  -v "$(pwd):/home/onhands-test/"  --name "onhands-alabama" "onhands-alabama" sh -c "cd tests; ./test.sh"
