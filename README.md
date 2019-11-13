# Ensembl-api

1.  How do I get set up this api? Install python +3.7 and create a virtualenv using pipenv:
    [See here how to](https://github.com/pypa/pipenv)

2.  Create and running a virtualenv
    ```
    user@server:~$ pipenv shell
    ```
3.  Running tests 
    ```
    user@server:~$ pipenv run pytest -v
    ```
4. Running api App:
    ```
    (ensembl-api-env) user@server:~$ FLAKS_APP=app.py
    (ensembl-api-env) user@server:~$ flask run
    ```
    
    The api will be available on http://127.0.0.1:5000/api/v1/gene
    
    A GET request example:
    ``` 
    http://127.0.0.1:5000/api/v1/gene?lookup=brc&species=africana
    ```
    Response example:
   
    ```
    {
        "results": [
            {
                "location": "scaffold_31:24570899-24632973",
                "species": "loxodonta_africana",
                "gene_name": "BRCA1",
                "ensembl_stable_id": "ENSLAFG00000021784"
            },
            {
                "location": "scaffold_11:4649923-4713848",
                "species": "loxodonta_africana",
                "gene_name": "BRCA2",
                "ensembl_stable_id": "ENSLAFG00000002670"
            },
            {
                "location": "scaffold_120:881888-941752",
                "species": "loxodonta_africana",
                "gene_name": "BRCC3",
                "ensembl_stable_id": "ENSLAFG00000013564"
            }
        ]
    }   
   
    ```
