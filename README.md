# PyWeb

Usefull if you need to add an HTTP command parser to your python script. HTTP requests are passed to a controller to be processed.

You can use the framework in this way:

    import commander
    

    def dummyFn(host, path):
        pass
    
    
    commander.start(dummyFn)

The _command_ module implements a cmd shell where you can send some commands to the application. The _start_ function starts the shell. You must pass a function to the commander, that function will be executed in response to each HTTP request.

When you start the _commander_, you are promt a command shell with the following commands available:

    (Cmd) help

    Documented commands (type help <topic>):
    ========================================
    exit  help  restart  start  status  stop

The _start_ command creates two new processed: the web and the controller. You can also use _start web_ or _start controller_.

Same considerations for the _stop_ command and the _restart_ command.

In every moment you can _start_, _stop_ or _restart_ the web module or the controller module.

If you type the _exit_ command, the main process and its children are terminated. If you kill the mail process, or something goes wrong and the main process is terminated, also the children processes commit suicide.

## Scenario

You start the application and you're presented the command prompt:

    MacBook-Air-di-Luca:pyweb bacchilu$ python commander.py 
    help per una lista dei comandi
    (Cmd) 

You start the processed:

    (Cmd) start
    web: 337
    controller: 338

The web process and the controller processes are shown with their pid.

Now, when you send HTTP requests, the callback function you configured is called with params _host_ and _path_.

If necessary you can check if everything is up and running:

    (Cmd) status
    web: 337
    controller: 338

Or you can terminate or restart a particular component:

    (Cmd) restart web
    web is down
    web: 339

The _exit_ command terminate all processes:

    (Cmd) exit
    web is down
    controller is down