<img src=".docs/logo.png" width="96px" align="right"/>

# AWS App

![License](https://img.shields.io/github/license/avcaliani/aws-app?logo=apache&color=lightseagreen)


Here you will find some PoCs that I've developed using AWS.

## Developer Airflow
First of all, build your own Airflow image. <br>
This command will add your AWS credentials to your Airflow container and automatically it will configure the default AWS connection.
```bash
docker-compose build \
  --build-arg ACCESS_KEY=$(cat ~/.aws/credentials | grep key_id | sed 's/.*key_id.*= //') \
  --build-arg SECRET_KEY=$(cat ~/.aws/credentials | grep secret | sed 's/.*secret.*= //')
```

Now, let's up a container with our image.
```bash
# Airflow will be deployed at "http://localhost:8080"
docker-compose up -d
```

When you finish using, just put down the container.
```bash
docker-compose down
```

### More Configurations

**Dags**<br>
At `docker-compose.yml` there are volumes pointing to every PoC DAG folder. 
If you have a new PoC and want to map your new DAG folder you have to create another volume mapping at `docker-compose.yml`.

**Default Variables**<br>
At `airflow/config/variables.json` you will find all variables that are going to be imported into Airflow at startup.
If you need to add another one, just add it to `variables.json` and rebuild the image.
**Be careful with secrets, I don't recommend to store these kind of values in this json file!**

