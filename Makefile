start:
	docker run -d -p 8000:8000 --name askgit askgit

stop:
	docker stop askgit

chat:
	./chat.sh
