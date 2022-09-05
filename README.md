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

![image](https://user-images.githubusercontent.com/6979641/188043629-b461fbef-fa3e-4f09-ae78-7d217613dc62.png)

Run the code bellow to check the STATUS of the clusters. All clusteres have to be "(healthy)":

```
$ docker ps
```

![image](https://user-images.githubusercontent.com/6979641/188043333-665ec5f9-bc21-4fe3-b9eb-a6f359d8e010.png)


## Chellange

To resolve this puzzel was used Airflow as orchestrator, PostgreSQL as DW, dbt to transform the data and Docker as environment.virtualizer.

To run the pipeline, acess the airflow with the link bellow, enter on "spark_etl" DAG and execute manually.


## Airflow credentials

Acess airflow on link: http://www.localhost:8080

__Login:__ airflow  
__Password:__ airflow

## PostgresSQL credentials

__Host:__ localhost  
__Port:__ 5432  
__Login:__ sparkns  
__Password:__ sparkns

## Improvements

### Airflow/DAG
1. To facilitate test execution, I code only one DAG. In a "real" situation I would split the DAG by HTTP calls. As we can use the data for others analysis, it is not indicate to create dependencies between endpoints. So, in one DAG, if the message endpoint goes down, the trusted data will not be avaliable for the analist.
2. A native e-mail alert should be used to warn about some failure.

### GDPR
It will be necessary to understand a little bit more the stakeholder goal to think about remove some PII data from the trusted layer.  


### Cloud

In order to have more secure an a more complete ecosytem, the use of Cloud would help to increase the possibilites of the project.

### DW

As mention above, cloud could bring us more performance, oportunities, scalability and security. Big Query and SnowFlake may be good option.

### DBT

Generics and single teste should be implemeted. Unique, not_null, accepted_values and relationships at least.  
Soda.io is an open-source and user-friendly Data Observability plataform whos woul increase the quality and trustability of our data. It is another option instead of dbt tests.

### Data Catalog

inever used a data catalog software yet, but Amundsen would be a good option to implement.
