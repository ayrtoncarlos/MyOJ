# MyOJ

Simple implementation of an online judge. 

Status: In development.

# Installation

## Set environment variables

### Python
[How to Install Python 3.9.7 on Windows 10 [ 2021 Update ] Complete Guide](https://www.youtube.com/watch?v=uSVl7gRXP80)

### C++
[How to Install MinGW | GCC Toolset for C and C++ Programming | Setting Path variable on Windows 10](https://www.youtube.com/watch?v=guM4XS43m4I)

### Java
[How To Download And Install Java on Windows 10 ( Java JDK on Windows 10) + Set JAVA_HOME](https://www.youtube.com/watch?v=_YmuR4aw9pM)

## Virtualenv

### Installing virtualenv
```
> pip install virtualenv
```

### Creating virtual environment
```
> python -m venv myoj
```

### Starting the virtual environment
```
> myoj\Scripts\activate
```

## Database

### Creating the database
```
(myoj): > cd .\project\
(myoj): > python
>>> from app import db, create_app
>>> db.create_all(app=create_app())
>>> exit()
```

## Start project
```
(myoj): > flask run
```