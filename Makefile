# build the container
container:
	docker build -t pysal .

# run jupyter notebook for development
nb:
	docker run --rm -p 8888:8888 -v ${PWD}:/home/jovyan/libpysal pysal

# run a shell for development
cli:
	docker run -it -p 8888:8888 -v ${PWD}:/home/jovyan pysal /bin/bash
