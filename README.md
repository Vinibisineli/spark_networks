# Spark Networks

## Requirements:
- Docker Compose v1.29.1 and newer.

#### Checking docker-compose version:
```
$ docker-compose version
```

### Upgrade docker-compose version:  
   
Uninstall you current docker-compose:  

https://docs.docker.com/compose/install/uninstall/

- Uninstall docker-compose on Ubuntu:
```
// If installed via apt-get
$ sudo apt-get remove docker-compose
// If installed via curl
$ sudo rm /usr/local/bin/docker-compose
//If installed via pip
$ pip uninstall docker-compose
```

https://docs.docker.com/desktop/linux/install/

- Installing docker-compose on Ubuntu:
```
$ apt-get install docker-compose
```


## 1st RUN:

On Linux, the quick-start needs to know your host user id:

```
$ echo -e "AIRFLOW_UID=$(id -u)" > .env
```

## Executing docker-compose

Execute in git-clone repositore folder:

```
$ docker compose up -d
```

Run the code bellow to check the STATUS of the clusters. All clusteres have to be "(healthy)":

```
$ docker ps
```

![image](https://user-images.githubusercontent.com/6979641/188043333-665ec5f9-bc21-4fe3-b9eb-a6f359d8e010.png)

## App

[TODO] Description

## Airflow credentials

Acess airflow on link: http://www.localhost:8080

__Login:__ airflow  
__Password:__ airflow

## PostgresSQL credentials

__Host:__ localhost  
__Port:__ 5432  
__Login:__ sparkns  
__Password:__ sparkns