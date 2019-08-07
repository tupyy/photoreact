
## Album 

**GET** */albums/*

	listeaza toate albumele pe care current_user poate sa le vizualizeze
	Filtre:
		- perioada: start, end
		- categorie: category
		- tag: tag

	Response:
		{
			{
				"id": "id album",
				"name": "name album",
				"description": "descriere album",
				"date": "data album",
				"preview": "URL preview photo S3",
				"categories" : [ "categorie_1", "categorie_2" ],
				"tags" : ["tag 1", "tag 2"]
			} 
		}

**GET** */album/{id}*
	
	listeaza continutul albumului {id}
    Response: 
		status_code = 200
			body:
				{
					"photos" : [ lista cu URL S3 presigned ale pozelor pe care utilizatorul are dreptul sa le vizualizeze
								{ 
									'id': 'id_poze',
									'url': 's3 url'
								},
								{ 
									'id': 'id poze',
									'url': 's3 url'
								}
				    ]
					"thumbnails" : [ list cu URL S3 presigned ale thumbnails pe care utilizatorul are dreptul sa le vizualizeze
										{ 
											'id': 'id_poze',
											'url': 's3 url'
										},
										{ 
											'id': 'id poze',
											'url': 's3 url'
										}
					               ]
					"permissions": [ list cu drepturi ale utilizatorului vezi #permissions ]
				}
		status_code = 403 FORBIDDEN daca nu are acces la album
		status_code = 404 Not found


*POST* **/album/**
	
	Creeaza album
	Request:
		{
			"name": "name album",
			"description": "descriere album",
			"date": "data album",
			"categories" : [ "categorie_1", "categorie_2" ],
			"tags" : ["tag 1", "tag 2"]
		}
	Reponse:
		status_code: 201 (CREATED)
			body: 
				{ "id": "id-ul noului album" }
		status_code: 403 FORBIDDEN 
			daca user-ul nu are voie sa creeze album


*DELETE* **/album/{id}**
	
	Sterge albumul {id}
	Response:
		status_code: 200 OK
		status_code: 403 FORBIDDEN daca nu are voie sa stearga albumul
		status_code: 404 Not found

*PUT* **/album/**
	
	Modifica album
	Request:
		{
			"id": "id album"
			"name": "name album",
			"description": "descriere album",
			"date": "data album",
			"categories" : [ "categorie_1", "categorie_2" ],
			"tags" : ["tag 1", "tag 2"]
		}
	Reponse:
		status_code: 200 (CREATED)
		status_code: 403 FORBIDDEN 
			daca user-ul nu are voie sa modifice albumul
		status_code: 404 Not found


## Photo
	
	Api-uri pentru poze

**POST** */photo/sign/*
	
	Sign S3 url pentru poze
	Request:
		{
			"album_id": "id-ul albumului",
			"filename": "numele pozei",
			"filetype": "tipul fisierului"
		}
	Reponse:
		status_code=200
		body:
			{
				"photo": "sign S3 url",
				"thumbnail": "sign S3 url pentru thumbnail"
			}
		status_code=403 daca utilizatorul nu are dreptul de a adauga poze
		status_code=404 daca album nu exista

**POST** */photo/*
	
	Adauga poza in album (in prealabil poza a fost uploadata in S3)
	Request:
		{
			"album_id": "id-ul albumului"
			"filename": "filename"
			"thumbnail: "numele thumbnail"
		}
	Response:
		status_code = 200 OK
		status_code = 403 daca utilizatorul nu are dreptul de a adauga poze
		status_code=404 daca album nu exista

**DELETE** */photo/{id}*
	
	Sterge poza 
	Response:
		- status_code = 200 OK
		- status_code = 403 FORBIDDEN
		- status_code = 404 Not found


