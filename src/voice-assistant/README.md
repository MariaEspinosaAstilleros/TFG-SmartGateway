## Rhasspy client

### Install
As a first step before using the Rhasspy client it's necessary to install the client library tpo communicate with the remote Rhasspy server
```shell
pi@raspberrypi:~$ pip3 install rhasspy-client
```

### Usage
Once the necessary library has been installed, we move on to the execution of the Rhasspy client. The only step to follow is to run the client with the audio input.

There are two ways of doing this, by running the client so that it picks up the user's real-time voice as audio input

```shell
pi@raspberrypi:~$ python3 rhasspy-client record
```

or by entering the audio file in *.wav* format via the argument line
```shell
pi@raspberrypi:~$ python3 rhasspy-client speech-to-text <nombre_audio>.wav
```