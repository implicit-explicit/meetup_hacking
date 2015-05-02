# meetup_hacking

A tool for visualising meetup information using Python and RickshawJS

### Development Environment

```
git clone https://github.com/implicit-explicit/meetup_hacking
cd meetup_hacking
vagrant up
vagrant ssh
cd /vagrant/code
```
You now have a CentOS7 VM with Python33 and you're ready to start running commands.

### Pulling member information for a group

1. First you need to generate your meetup API key at https://secure.meetup.com/meetup_api/key/
2. Then get the _url_name_ of the meetup group you would like to query. This is the name in the URL when you're looking at it in your browser. So for example the _url_name_ for the [Software Circus](http://www.meetup.com/Software-Circus/) meetup group would be 'Software-Circus'
3. Then you can run [meetup_members.py](https://github.com/implicit-explicit/meetup_hacking/blob/master/code/meetup_members.py)

```
./meetup_members.py <YOUR API KEY> <url_name> [Number of members to pull per batch]
```

This will write the member information for the specified group to _stdout_.

### Preparing member information for visualisation

Now you have the member data for the specified group but before you have display this you will need to preprocess it first.

1. Pipe the output of the first command into [members_over_time.py](https://github.com/implicit-explicit/meetup_hacking/blob/master/code/members_over_time.py).
```
./meetup_members.py <YOUR API KEY> <url_name> [Number of members to pull per batch] | ./members_over_time.py
```
2. The results will be written to _stdout_. Better to stick them in a file for now.
```
./meetup_members.py <YOUR API KEY> <url_name> [Number of members to pull per batch] | ./members_over_time.py > <url_name>.json
```

### Displaying your results

1. Copy your new JSON file into the _data_ directory
```
mkdir visualisation/data
cp <url_name>.json visualisation/data
cd visualisation
python -m SimpleHTTPServer
```
2. Then in a browser navigate to http://localhost:8000/members.html
3. Kaboom!

