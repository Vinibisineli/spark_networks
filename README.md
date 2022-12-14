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
$ docker-compose up -d
```

![image](https://user-images.githubusercontent.com/6979641/188043629-b461fbef-fa3e-4f09-ae78-7d217613dc62.png)

Run the code bellow to check the STATUS of the clusters. All clusteres have to be "(healthy)":

```
$ docker ps
```

![image](https://user-images.githubusercontent.com/6979641/188043333-665ec5f9-bc21-4fe3-b9eb-a6f359d8e010.png)


## Challenge

To resolve this puzzle was used Airflow as orchestrator, PostgreSQL as DW, dbt to transform the data and Docker as environment.virtualizer.

Airflow is important to orchestrator the pipelines and their dependencies, monitoring and alerting in case of any failure. After dozens of DAGs, it becomes impossible whitout a service like that.

Postgre is not the best option for DW. I will comment better options of DW on the [Improvements](#improvements) section.

DBT is a good open-source option to organize, tranform, test and document our pipelines.

Docker is essential to ensure enviroment will always be functional on ever place we run it.

To run the pipeline, acess the airflow with the link bellow, enter on "spark_etl" DAG and execute manually.


### ETL - Airflow
![image](https://user-images.githubusercontent.com/6979641/188530508-69c30882-54af-4e7c-ae06-64e472271a57.png)

### DBT Lineage
![image](https://user-images.githubusercontent.com/6979641/188532820-33fcca41-cc28-4c54-8e92-e085a210ba06.png)

- To generate DBT docs will be need to enter on airflow container running:

```
$ docker exec -it spark_networks-airflow-webserver-1 /bin/bash
```
   
After run the code:

```
dbt docs generate
```

and then:

```
dbt docs serve --port 8098
```

So will be able to acess http://localhost:8090



## Airflow credentials

Acess airflow on link: http://www.localhost:8080

__Login:__ airflow  
__Password:__ airflow

## PostgresSQL credentials

__Host:__ localhost  
__Port:__ 5432  
__Login:__ sparkns  
__Password:__ sparkns

## Folder Structure

- dags - where the DAGs and other Python scripts nedd to be
  - data - path to salve data extract from DAG 
  - script - Python scripts use on DAGs 
- dbt - files used by dbt to generate data transformation
  - models
    - anonymize - model to hasg some PII values
    - rename - model to rename columns
    - trusted - model to generate data to DA
- plugins 
  - sql - place to store .sql files used on DAGs  


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

I never used a data catalog software yet, but Amundsen would be a good option to implement.
