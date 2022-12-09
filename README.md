### Backend Project 3

| Group 10         |
| ---------------- |
| Mohamed Habarneh |
| Mayur Kolhe      |
| Marina Urrutia   |
| Mike Ploythai    |

##### HOW TO RUN THE PROJECT

0. Install the following dependencies

```
   // nginx and nginx-extras
   sudo apt-get install nginx nginx-extras

   // redis-server
   sudo apt-get install redis-server

   // redis
   pip install redis

   // hiredis
   pip install hiredis
```

1. Copy the contents of our [nginx config file](https://github.com/mploythai/Web-Back-End-Project3/blob/master/nginxconfig.txt) into a new file within `/etc/nginx/sites-enabled` called `nginxconfig`. Assuming the nginx service is already running, restart the service using `sudo service nginx restart`.

   Additionally, start the redis server with `sudo service redis start`

2. Initialize the databases within the project folder

   ```c
      // step 1. give the script permissions to execute
      chmod +x ./bin/start.sh

      // step 2. run the script
      ./bin/start.sh

      // step 3. start the server
      foreman start

      // step 4. give the script permissions to execute
      chmod +x ./bin/init.sh

      // step 5. run the script
      ./bin/init.sh
   ```

3. Populate the word databases

   ```c
      python3 dbpop.py
   ```

4. Test all the endpoints using httpie

   - user

     - register account: `http POST http://tuffix-vm/registration username="yourusername" password="yourpassword"`

     Sample Output:

     ```
     {
       "id": 3,
       "password": "tawade",
       "username": "himani"
     }
     ```

     - login {Not accesible}: 'http --auth himani:tawade GET http://tuffix-vm/login'
       Sample Output:

     ```
      HTTP/1.1 404 Not Found
      Connection: keep-alive
      Content-Encoding: gzip
      Content-Type: text/html
      Date: Fri, 18 Nov 2022 21:04:31 GMT
      Server: nginx/1.18.0 (Ubuntu)
      Transfer-Encoding: chunked

      <html>
      <head><title>404 Not Found</title></head>
      <body>
      <center><h1>404 Not Found</h1></center>
      <hr><center>nginx/1.18.0 (Ubuntu)</center>
      </body>
      </html>
     ```

   - game

     - create a new game: `http --auth yourusername:yourpassword POST http://tuffix-vm/newgame`

     Sample Output:

     ```
     'http --auth himani:tawade POST http://tuffix-vm/newgame'
     {
        "answerid": 3912,
        "gameid": "b0039f36-6784-11ed-ba4a-615e339a8400",
        "username": "himani"
     }
     ```

     Note - this will return a `gameid`

     - add a guess: `http --auth yourusername:yourpassword PUT http://tuffix-vm/addguess gameid="gameid" word="yourguess"`

     Sample Output:

     ```
     http --auth himani:tawade PUT http://tuffix-vm/addguess gameid="b0039f36-6784-11ed-ba4a-615e339a8400" word="amigo"
     {
        "Accuracy": "XXOOO",
        "guessedWord": "amigo"
     }
     ```

     - display your active games: `http --auth yourusername:yourpassword GET http://tuffix-vm/allgames`

     Sample Output:

     ```
     http --auth himani:tawade GET http://tuffix-vm/allgames
     [
        {
           "gameid": "b0039f36-6784-11ed-ba4a-615e339a8400",
           "gstate": "In-progress",
           "guesses": 1
        }
     ]
     ```

     - display the game status and stats for one game: `http --auth yourusername:yourpassword GET http://tuffix-vm/onegame?id=gameid`
       - example: `.../onegame?id=b97fcbb0-6717-11ed-8689-e9ba279d21b6`

     Sample Output:

     ```
     http --auth himani:tawade GET http://tuffix-vm/onegame?id="b0039f36-6784-11ed-ba4a-615e339a8400"
     [
        {
              "gameid": "b0039f36-6784-11ed-ba4a-615e339a8400",
           "gstate": "In-progress",
           "guesses": 1
           },
           {
              "accuracy": "XXOOO",
              "guessedword": "amigo"
           }
     ]
     ```

     - return the results of a game (win or loss), along with the number of guesses the user made: `http POST http://127.0.0.1:5400/postgame`

     Sample Output:

     ```
        http POST http://127.0.0.1:5400/postgame
        {
           "username1": 3,
           "username10": 0,
           "username11": 0,
           "username12": 0,
           "username13": 0,
           "username14": 2,
           "username15": 1,
           "username16": 3,
           "username17": 5,
           "username18": 0,
           "username19": 0,
           "username2": 3,
           "username3": 0,
           "username4": 2,
           "username5": 2,
           "username6": 0,
           "username7": 1,
           "username8": 0,
           "username9": 0
        }
     ```

     - retrieve the top 10 users by average score: `http GET http://tuffix-vm/leaderboard`
       - if you're not running on Ubuntu, you must add `:5400` to the end of `tuffix-vm`

     Sample Output:

     ```
        http GET http://tuffix-vm/leaderboard
        {
           "username1": 6,
           "username14": 1,
           "username17": 4,
           "username2": 4,
           "username4": 0,
           "username5": 4,
           "username6": 0,
           "username7": 0,
           "username8": 0,
           "username9": 0
        }
     ```

5. to close the server, do `ctrl + c`. After the server closes, unmount the databases

   ```
      // give permissions
      chmod +x ./bin/unmount.sh

      // run
      ./bin/unmount.sh
   ```
