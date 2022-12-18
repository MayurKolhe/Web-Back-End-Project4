### Backend Project 4

| Group 12         |
| ---------------- |
| Satish Bisa |
| Mayur Kolhe      |
| Debdyuti Das   |
| Henry Nguyen    |

##### PROJECT OVERVIEW
This project builds off of a previous project 3 build, with some additional functionality such as webhook usage, message deliveries via Redis Queue queues, and UNIX cron service implementation. Details on webhook implementation can be seen in the foreman output throughout the execution of the game service's endpoint executions (specifically /addguess). Upon the completion of a game, foreman will also show information regarding the worker function being used for the message queue's job execution. In particular, it shows the successful completion of outputting a leaderboard after the leaderboard service receives information from the game service. And for the UNIX cron implementation, details can simply be seen by executing the following commands (in order) from the project's directory:

```
   crontab -e

   cd /var/log

   vi syslog
   
```


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

4. Restart foreman

 ```c
     *ctrl + c*
     foreman start
   ```
   NOTE 1: We found during testing that this step is helpful for the callback URL data to be seen from the DB.
   NOTE 2: If an error occurs on this command, run "sudo lsof -i :5100" and stop any relevant PIDs with "kill -9 (*pid value*)"

5. Test all the endpoints using httpie

   - user

     - register account: `http POST http://127.0.0.1:5000/registration  username="yourusername" password="yourpassword"`

     Sample Output:

     ```
     {
       "id": 1,
       "password": "abc",
       "username": "abc"
     }
     ```

     - login: 'http --auth abc:abc GET http://127.0.0.1:5000/login'
       Sample Output:

     ```
      HTTP/1.1 200 
      content-length: 24
      content-type: application/json
      date: Sun, 18 Dec 2022 02:23:36 GMT
      server: hypercorn-h11

      {
         "authenticated": "true"
      }

     ```

   - game

     - create a new game: `http --auth username:password POST http://127.0.0.1:5100/newgame`

     Sample Output:

     ```
     'http --auth abc:abc POST http://127.0.0.1:5100/newgame'
     {
        "answerid": 1380,
        "gameid": "9d0e068e-7e75-11ed-afbc-fba81ab2d100",
        "username": "abc"
     }
     ```

     NOTE: the "gameid" value returned here is important to re-use for commands which apply to that specific game i.e. guessing      a word for a particular game. 

     - Take a guess: `http --auth username:password PUT http://127.0.0.1:5100/addguess gameid="gameid" word="yourguess"`

     Sample Output:

     ```
     http --auth abc:abc PUT http://127.0.0.1:5100/addguess gameid=9d0e068e-7e75-11ed-afbc-fba81ab2d100 word=money
     {
        "Accuracy": "XXOXO",
        "guessedWord": "money"
     }
     ```
     NOTE: Once game is finished, foreman will output details on the worker function which the game service uses to send score      information to the leaderboard service upon game completion. Also, under the specific leaderboard messages on foreman, you      will be able to see successful '200' messages as well as relevant webhook details. 

     - display your active games: `http --auth yourusername:yourpassword GET http://127.0.0.1:5100/allgames`

     Sample Output:

     ```
     http --auth abc:abc GET http://127.0.0.1:5100/allgames
     [
        {
           "gameid": "9d0e068e-7e75-11ed-afbc-fba81ab2d100",
           "gstate": "In-progress",
           "guesses": 1
        }
     ]
     ```

     - Display the game status and stats for a particular game: `http --auth username:password GET http://127.0.0.1:5100/onegame?id=gameid`

     Sample Output:

     ```
     http --auth abc:abc GET http://127.0.0.1:5100/onegame?id="9d0e068e-7e75-11ed-afbc-fba81ab2d100"
     [
        {
              "gameid": "b0039f36-6784-11ed-ba4a-615e339a8400",
           "gstate": "In-progress",
           "guesses": 1
           },
           {
              "accuracy": "XXOXO",
              "guessedword": "money"
           }
     ]
     ```

     - Show the top 10 leaders of all games with 'http GET http://127.0.0.1:5400/leaderboard'

     Sample Output:

     ```
        Top 10 leaders are:
        
        'abc', 5.0
        'def', 5.0
        'ghi', 5.0
        'jkl', 5.0
        'mno', 5.0
        'pqr', 5.0
        'stu', 5.0
        'vwx', 5.0
        'yza', 5.0
        'bcd', 5.0
     ```

5. to close the server, run `ctrl + c`. After the server closes, unmount the databases

   ```
      // give permissions
      chmod +x ./bin/unmount.sh

      // run
      ./bin/unmount.sh
   ```
