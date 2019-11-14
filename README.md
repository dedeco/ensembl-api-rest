# Ensembl Api for search genes

The putative “Ensembl Services Platform” allows users to search for a gene by its name. One web REST service
is available on this platform to get all gene names corresponding to a pattern.

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
    
    The api will be available on http://127.0.0.1:5000/api/v1/genes
    
    A GET request example
    
    ``` 
    http://127.0.0.1:5000/api/v1/genes?lookup=brc&species=sapiens&limit=3
    ```

      - LIMIT: 3
      - Gene name lookup: "brc"
      - Species: "sapiens"

    Response example:
    
   ```
    {
        "start": 1,
        "limit": 3,
        "count": 4,
        "previous": "",
        "next": "/api/v1/genes?start=4&limit=3&lookup=brc&species=sapiens",
        "results": [
            {
                "species": "homo_sapiens",
                "ensembl_stable_id": "ENSG00000012048",
                "gene_name": "BRCA1",
                "location": "17:43044295-43170245"
            },
            {
                "species": "homo_sapiens",
                "ensembl_stable_id": "ENSG00000139618",
                "gene_name": "BRCA2",
                "location": "13:32315474-32400266"
            },
            {
                "species": "homo_sapiens",
                "ensembl_stable_id": "ENSG00000185515",
                "gene_name": "BRCC3",
                "location": "X:155071420-155123074"
            }
        ]
    }
   ```
